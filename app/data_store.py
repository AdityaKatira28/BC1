import json
import os
from typing import List
from app.models import ComplianceCheck
from datetime import datetime

class DataStore:
    def __init__(self, storage_file: str = "compliance_data.json"):
        self.storage_file = storage_file
        self._store: List[ComplianceCheck] = []
        self.load_data()
    
    def load_data(self):
        """Load data from file if it exists"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self._store = [ComplianceCheck(**item) for item in data]
                print(f"Loaded {len(self._store)} records from {self.storage_file}")
            except Exception as e:
                print(f"Error loading data from {self.storage_file}: {e}")
                self._store = []
        else:
            self._store = []
    
    def save_data(self):
        """Save data to file"""
        try:
            # Convert ComplianceCheck objects to dictionaries for JSON serialization
            data = []
            for item in self._store:
                item_dict = item.dict()
                # Convert datetime to string for JSON serialization
                if isinstance(item_dict['last_checked'], datetime):
                    item_dict['last_checked'] = item_dict['last_checked'].isoformat()
                data.append(item_dict)
            
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Saved {len(self._store)} records to {self.storage_file}")
        except Exception as e:
            print(f"Error saving data to {self.storage_file}: {e}")
    
    def set_data(self, records: List[ComplianceCheck]):
        """Set new data and save to file"""
        self._store = records
        self.save_data()
    
    def get_data(self) -> List[ComplianceCheck]:
        """Get current data"""
        return self._store
    
    def clear_data(self):
        """Clear all data"""
        self._store = []
        self.save_data()
    
    def is_empty(self) -> bool:
        """Check if store is empty"""
        return len(self._store) == 0

# Global instance
data_store = DataStore()