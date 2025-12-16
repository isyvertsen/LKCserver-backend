#!/usr/bin/env python3
"""
Database Anonymization Migration Script

This script provides a comprehensive database anonymization solution for the entire database,
with special focus on the tblkunder (customers) table and other tables containing PII.
"""

import asyncio
import logging
import sys
from typing import Dict, List, Optional, Any
from datetime import datetime
from faker import Faker
from faker.providers import internet, phone_number
from sqlalchemy import select, update, text
from sqlalchemy.ext.asyncio import AsyncSession

# Add the backend directory to Python path for imports
sys.path.append('/Users/ivarsyvertsen/code/ravi/LKCserver/catering-system/backend')

from app.infrastructure.database.session import AsyncSessionLocal
from app.models.kunder import Kunder
from app.models.ansatte import Ansatte

# Initialize Faker with Norwegian locale
fake = Faker('no_NO')
fake.add_provider(internet)
fake.add_provider(phone_number)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('anonymization_migration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DatabaseAnonymizer:
    """Handles comprehensive database anonymization."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.fake = fake
        self.stats = {
            'start_time': datetime.now(),
            'tables_processed': 0,
            'total_records_processed': 0,
            'successful_anonymizations': 0,
            'failed_anonymizations': 0,
            'errors': []
        }
    
    async def anonymize_entire_database(self, kundegruppe: Optional[int] = None) -> Dict[str, Any]:
        """
        Anonymize all sensitive data in the entire database.
        
        Args:
            kundegruppe: Optional customer group ID to filter customers by
        
        Returns:
            Dict: Comprehensive statistics about the anonymization process
        """
        filter_msg = f" (customers filtered by kundegruppe {kundegruppe})" if kundegruppe else ""
        logger.info(f"Starting comprehensive database anonymization{filter_msg}")
        
        try:
            # Anonymize customers (tblkunder) - with optional filtering
            await self._anonymize_customers(kundegruppe)
            
            # Anonymize employees (tblansatte) - always all employees
            await self._anonymize_employees()
            
            # Add more table anonymizations as needed
            # await self._anonymize_other_tables()
            
            self.stats['end_time'] = datetime.now()
            self.stats['duration'] = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
            
            logger.info(f"Database anonymization completed successfully: {self.stats}")
            return self.stats
            
        except Exception as e:
            self.stats['errors'].append(str(e))
            logger.error(f"Error in database anonymization: {str(e)}")
            await self.session.rollback()
            return self.stats
    
    async def _anonymize_customers(self, kundegruppe: Optional[int] = None) -> None:
        """Anonymize customer data in tblkunder, optionally filtered by kundegruppe."""
        filter_msg = f" in kundegruppe {kundegruppe}" if kundegruppe else ""
        logger.info(f"Starting customer anonymization{filter_msg}")
        
        try:
            # Build query with optional kundegruppe filter
            query = select(Kunder.kundeid)
            if kundegruppe is not None:
                query = query.where(Kunder.kundegruppe == kundegruppe)
            
            result = await self.session.execute(query)
            customer_ids = [row[0] for row in result.fetchall()]
            
            batch_size = 100
            processed = 0
            
            for i in range(0, len(customer_ids), batch_size):
                batch_ids = customer_ids[i:i + batch_size]
                
                for customer_id in batch_ids:
                    try:
                        anonymized_data = self._generate_customer_anonymized_data()
                        
                        await self.session.execute(
                            update(Kunder)
                            .where(Kunder.kundeid == customer_id)
                            .values(**anonymized_data)
                        )
                        
                        self.stats['successful_anonymizations'] += 1
                        processed += 1
                        
                    except Exception as e:
                        self.stats['failed_anonymizations'] += 1
                        self.stats['errors'].append(f"Customer {customer_id}: {str(e)}")
                        logger.error(f"Error anonymizing customer {customer_id}: {str(e)}")
                
                await self.session.commit()
                logger.info(f"Processed customer batch: {processed}/{len(customer_ids)}")
            
            self.stats['tables_processed'] += 1
            self.stats['total_records_processed'] += len(customer_ids)
            logger.info(f"Customer anonymization completed: {len(customer_ids)} records processed{filter_msg}")
            
        except Exception as e:
            logger.error(f"Error in customer anonymization: {str(e)}")
            self.stats['errors'].append(f"Customer anonymization: {str(e)}")
            await self.session.rollback()
    
    async def _anonymize_employees(self) -> None:
        """Anonymize employee data in tblansatte."""
        logger.info("Starting employee anonymization")
        
        try:
            # Get all employee IDs
            result = await self.session.execute(select(Ansatte.ansattid))
            employee_ids = [row[0] for row in result.fetchall()]
            
            batch_size = 50
            processed = 0
            
            for i in range(0, len(employee_ids), batch_size):
                batch_ids = employee_ids[i:i + batch_size]
                
                for employee_id in batch_ids:
                    try:
                        anonymized_data = self._generate_employee_anonymized_data()
                        
                        await self.session.execute(
                            update(Ansatte)
                            .where(Ansatte.ansattid == employee_id)
                            .values(**anonymized_data)
                        )
                        
                        self.stats['successful_anonymizations'] += 1
                        processed += 1
                        
                    except Exception as e:
                        self.stats['failed_anonymizations'] += 1
                        self.stats['errors'].append(f"Employee {employee_id}: {str(e)}")
                        logger.error(f"Error anonymizing employee {employee_id}: {str(e)}")
                
                await self.session.commit()
                logger.info(f"Processed employee batch: {processed}/{len(employee_ids)}")
            
            self.stats['tables_processed'] += 1
            self.stats['total_records_processed'] += len(employee_ids)
            logger.info(f"Employee anonymization completed: {len(employee_ids)} records processed")
            
        except Exception as e:
            logger.error(f"Error in employee anonymization: {str(e)}")
            self.stats['errors'].append(f"Employee anonymization: {str(e)}")
            await self.session.rollback()
    
    def _generate_customer_anonymized_data(self) -> Dict[str, Any]:
        """Generate anonymized data for customers."""
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        
        return {
            'kundenavn': f"{first_name} {last_name}",
            'kontaktid': self.fake.uuid4()[:20],
            'telefonnummer': self.fake.phone_number(),
            'adresse': self.fake.street_address(),
            'postboks': self.fake.random_int(min=1, max=9999) if self.fake.boolean(chance_of_getting_true=30) else None,
            'postnr': self.fake.postcode(),
            'sted': self.fake.city(),
            'e_post': self.fake.email(),
            'e_post2': self.fake.email() if self.fake.boolean(chance_of_getting_true=20) else None,
            'mobilnummer': self.fake.phone_number(),
            'webside': f"https://www.{self.fake.domain_name()}" if self.fake.boolean(chance_of_getting_true=40) else None,
            'merknad': self._generate_fake_note(),
            'menyinfo': self._generate_fake_menu_info(),
        }
    
    def _generate_employee_anonymized_data(self) -> Dict[str, Any]:
        """Generate anonymized data for employees."""
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        
        return {
            'ansattnavn': f"{first_name} {last_name}",
            'brukernavn': f"{first_name.lower()}.{last_name.lower()}",
            'telefonnummer': self.fake.phone_number() if self.fake.boolean(chance_of_getting_true=80) else None,
            'e_post': self.fake.email(),
            'mobilnummer': self.fake.phone_number() if self.fake.boolean(chance_of_getting_true=90) else None,
        }
    
    def _generate_fake_note(self) -> Optional[str]:
        """Generate a fake note/remark."""
        if not self.fake.boolean(chance_of_getting_true=60):
            return None
        
        notes = [
            "Vanlig levering",
            "Ring før levering", 
            "Levering ved bakdør",
            "Kontakt vaktmester",
            "Spesielle leveringsinstruksjoner",
            "Levering mellom 10-12",
            "Kun ukedager",
        ]
        return self.fake.random_element(notes)
    
    def _generate_fake_menu_info(self) -> Optional[str]:
        """Generate fake menu information."""
        if not self.fake.boolean(chance_of_getting_true=40):
            return None
        
        menu_info = [
            "Standard meny",
            "Vegetarisk alternativ", 
            "Glutenfri meny",
            "Laktosefri alternativ",
            "Diabetikermeny",
            "Energirik kost",
        ]
        return self.fake.random_element(menu_info)
    
    async def create_backup_before_anonymization(self) -> bool:
        """
        Create a backup of sensitive data before anonymization.
        This is crucial for potential data recovery if needed.
        """
        try:
            logger.info("Creating backup of sensitive data")
            
            # Create backup tables
            backup_tables = [
                ("tblkunder_backup", "tblkunder"),
                ("tblansatte_backup", "tblansatte")
            ]
            
            for backup_table, original_table in backup_tables:
                # Drop backup table if it exists
                await self.session.execute(text(f"DROP TABLE IF EXISTS {backup_table}"))
                
                # Create backup table with current data
                await self.session.execute(text(f"""
                    CREATE TABLE {backup_table} AS 
                    SELECT * FROM {original_table}
                """))
                
                logger.info(f"Created backup table: {backup_table}")
            
            await self.session.commit()
            logger.info("Backup creation completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error creating backup: {str(e)}")
            await self.session.rollback()
            return False
    
    async def verify_anonymization(self) -> Dict[str, Any]:
        """
        Verify that anonymization was successful by checking for common patterns.
        
        Returns:
            Dict: Verification results
        """
        logger.info("Starting anonymization verification")
        
        verification_results = {
            'customers_checked': 0,
            'employees_checked': 0,
            'potential_issues': [],
            'verification_passed': True
        }
        
        try:
            # Check customers for common Norwegian names or patterns that might indicate incomplete anonymization
            common_norwegian_names = ['Ola', 'Kari', 'Per', 'Anne', 'Lars', 'Ingrid', 'Bjørn', 'Astrid']
            
            for name in common_norwegian_names:
                result = await self.session.execute(
                    select(Kunder.kundeid).where(Kunder.kundenavn.ilike(f"%{name}%"))
                )
                matching_customers = result.fetchall()
                
                if len(matching_customers) > 10:  # If too many customers have the same common name
                    verification_results['potential_issues'].append(
                        f"Found {len(matching_customers)} customers with name containing '{name}'"
                    )
            
            # Check for email patterns that might indicate incomplete anonymization
            result = await self.session.execute(
                select(Kunder.kundeid).where(Kunder.e_post.ilike("%@larvik.kommune.no"))
            )
            municipality_emails = result.fetchall()
            
            if len(municipality_emails) > 0:
                verification_results['potential_issues'].append(
                    f"Found {len(municipality_emails)} customers with municipality email addresses"
                )
            
            # Get counts
            customer_count = await self.session.execute(select(Kunder.kundeid))
            verification_results['customers_checked'] = len(customer_count.fetchall())
            
            employee_count = await self.session.execute(select(Ansatte.ansattid))
            verification_results['employees_checked'] = len(employee_count.fetchall())
            
            if verification_results['potential_issues']:
                verification_results['verification_passed'] = False
            
            logger.info(f"Verification completed: {verification_results}")
            return verification_results
            
        except Exception as e:
            logger.error(f"Error in verification: {str(e)}")
            verification_results['potential_issues'].append(f"Verification error: {str(e)}")
            verification_results['verification_passed'] = False
            return verification_results


async def run_full_database_anonymization(create_backup: bool = True, kundegruppe: Optional[int] = None) -> Dict[str, Any]:
    """
    Run complete database anonymization with backup and verification.
    
    Args:
        create_backup: Whether to create backup tables before anonymization
        kundegruppe: Optional customer group ID to filter customers by
        
    Returns:
        Dict: Complete anonymization results
    """
    results = {
        'backup_created': False,
        'anonymization_stats': {},
        'verification_results': {},
        'overall_success': False,
        'kundegruppe_filter': kundegruppe
    }
    
    async with AsyncSessionLocal() as session:
        anonymizer = DatabaseAnonymizer(session)
        
        try:
            # Create backup if requested
            if create_backup:
                results['backup_created'] = await anonymizer.create_backup_before_anonymization()
                if not results['backup_created']:
                    logger.error("Backup creation failed. Aborting anonymization.")
                    return results
            
            # Run anonymization
            results['anonymization_stats'] = await anonymizer.anonymize_entire_database(kundegruppe)
            
            # Verify anonymization
            results['verification_results'] = await anonymizer.verify_anonymization()
            
            # Determine overall success
            results['overall_success'] = (
                results['anonymization_stats'].get('failed_anonymizations', 0) == 0 and
                results['verification_results'].get('verification_passed', False)
            )
            
            logger.info(f"Complete anonymization process finished: {results}")
            return results
            
        except Exception as e:
            logger.error(f"Error in full anonymization process: {str(e)}")
            results['anonymization_stats'] = {'errors': [str(e)]}
            return results


async def main():
    """Main function for running the migration script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Database anonymization migration script')
    parser.add_argument('--no-backup', action='store_true', help='Skip backup creation (not recommended)')
    parser.add_argument('--verify-only', action='store_true', help='Only run verification checks')
    parser.add_argument('--kundegruppe', type=int, help='Filter customers by kundegruppe ID')
    
    args = parser.parse_args()
    
    if args.verify_only:
        logger.info("Running verification checks only")
        async with AsyncSessionLocal() as session:
            anonymizer = DatabaseAnonymizer(session)
            verification_results = await anonymizer.verify_anonymization()
            print(f"Verification results: {verification_results}")
    else:
        create_backup = not args.no_backup
        
        if args.no_backup:
            logger.warning("Running anonymization WITHOUT backup - this is not recommended!")
            confirmation = input("Are you sure you want to proceed without backup? (yes/no): ")
            if confirmation.lower() != 'yes':
                logger.info("Anonymization cancelled by user")
                return
        
        filter_msg = f" for kundegruppe {args.kundegruppe}" if args.kundegruppe else ""
        logger.info(f"Starting full database anonymization{filter_msg}")
        results = await run_full_database_anonymization(create_backup, args.kundegruppe)
        
        print("=" * 60)
        print("DATABASE ANONYMIZATION RESULTS")
        print("=" * 60)
        print(f"Backup created: {results['backup_created']}")
        print(f"Overall success: {results['overall_success']}")
        print(f"Anonymization stats: {results['anonymization_stats']}")
        print(f"Verification results: {results['verification_results']}")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())