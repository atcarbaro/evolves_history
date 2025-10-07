import pandas as pd
from typing import List, Dict, Any
import json


class DigimonEvolutionService:
    """Service to query Digimon evolution lines"""
    
    def __init__(self, excel_path: str):
        """
        Initialize the service by loading the Excel file
        
        Args:
            excel_path: Path to the Excel file with Digimon data
        """
        self.excel_path = excel_path
        self.df = None
        self._load_data()
    
    def _load_data(self):
        """Load data from Excel into a pandas DataFrame"""
        try:
            self.df = pd.read_excel(self.excel_path)
            
            # Verify required base columns
            base_columns = ['Number', 'Name', 'Stage', 'Attribute']
            missing_columns = [col for col in base_columns if col not in self.df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            print(f"✓ File loaded successfully: {len(self.df)} Digimon found")
            
        except Exception as e:
            raise Exception(f"Error loading Excel file: {str(e)}")
    
    def _get_evolutions_from_row(self, row: pd.Series) -> List[str]:
        """
        Extract all evolutions from a DataFrame row.
        Evolutions can be in the 'Evolutions' column and additional columns.
        
        Args:
            row: DataFrame row
            
        Returns:
            List of Digimon names (evolutions)
        """
        evolutions = []
        
        # Get all columns that could contain evolutions
        # Starting with 'Evolutions' and then unnamed columns
        evolution_columns = ['Evolutions'] + [col for col in row.index if 'Unnamed' in str(col)]
        
        for col in evolution_columns:
            if col in row.index:
                value = row[col]
                # Only add non-null and non-empty values
                if pd.notna(value) and str(value).strip() != '':
                    evolutions.append(str(value).strip())
        
        return evolutions
    
    def _find_previous_evolutions(self, digimon_name: str) -> List[Dict[str, Any]]:
        """
        Find Digimon that evolve into the given Digimon (pre-evolutions)
        
        Args:
            digimon_name: Name of the Digimon to search
            
        Returns:
            List of dictionaries with pre-evolution information
        """
        previous_evolutions = []
        digimon_name_lower = digimon_name.lower()
        
        for _, row in self.df.iterrows():
            evolutions = self._get_evolutions_from_row(row)
            
            # If the searched digimon is in this row's evolutions
            if any(digimon_name_lower == evo.lower() for evo in evolutions):
                previous_evolutions.append({
                    'name': row['Name'],
                    'stage': row['Stage'],
                    'number': int(row['Number']) if pd.notna(row['Number']) else None
                })
        
        return previous_evolutions
    
    def _find_next_evolutions(self, digimon_row: pd.Series) -> List[Dict[str, Any]]:
        """
        Find evolutions of the given Digimon (post-evolutions)
        
        Args:
            digimon_row: DataFrame row with Digimon data
            
        Returns:
            List of dictionaries with evolution information
        """
        evolutions_names = self._get_evolutions_from_row(digimon_row)
        next_evolutions = []
        
        for evo_name in evolutions_names:
            # Search for evolution Digimon information
            evo_data = self.df[self.df['Name'].str.lower() == evo_name.lower()]
            
            if not evo_data.empty:
                evo_row = evo_data.iloc[0]
                next_evolutions.append({
                    'name': evo_row['Name'],
                    'stage': evo_row['Stage'],
                    'number': int(evo_row['Number']) if pd.notna(evo_row['Number']) else None
                })
            else:
                # If complete information is not found, add only the name
                next_evolutions.append({
                    'name': evo_name,
                    'stage': None,
                    'number': None
                })
        
        return next_evolutions
    
    def get_evolution_line(self, digimon_name: str) -> str:
        """
        Get complete evolution line for a Digimon
        
        Args:
            digimon_name: Name of the Digimon to search
            
        Returns:
            JSON string with evolution line in the format:
            {
              "currentDigimon": { "name": "...", "number": 1, "stage": "...", "attribute": "..." },
              "preEvolutions": [...],
              "postEvolutions": [...]
            }
        """
        # Search for the Digimon (case-insensitive)
        digimon_matches = self.df[self.df['Name'].str.lower() == digimon_name.lower()]
        
        if digimon_matches.empty:
            return json.dumps({
                'error': True,
                'message': f'Digimon not found: {digimon_name}'
            }, indent=2, ensure_ascii=False)
        
        results = []
        
        # There may be multiple matches (same name, different forms)
        for _, digimon_row in digimon_matches.iterrows():
            # Get previous evolutions (de-evolutions)
            previous_evolutions = self._find_previous_evolutions(digimon_row['Name'])
            
            # Get next evolutions
            next_evolutions = self._find_next_evolutions(digimon_row)
            
            result = {
                'currentDigimon': {
                    'name': digimon_row['Name'],
                    'number': int(digimon_row['Number']) if pd.notna(digimon_row['Number']) else None,
                    'stage': digimon_row['Stage'],
                    'attribute': digimon_row['Attribute']
                },
                'preEvolutions': previous_evolutions,
                'postEvolutions': next_evolutions
            }
            
            results.append(result)
        
        # If there's only one result, return that object directly
        # If there are multiple, return array
        if len(results) == 1:
            response = results[0]
        else:
            response = {
                'message': f'Found {len(results)} results for: {digimon_name}',
                'results': results
            }
        
        return json.dumps(response, indent=2, ensure_ascii=False)
    
    def get_evolution_line_dict(self, digimon_name: str) -> Dict[str, Any]:
        """
        Alternative version that returns a dictionary instead of JSON string
        
        Args:
            digimon_name: Name of the Digimon to search
            
        Returns:
            Dictionary with evolution line
        """
        return json.loads(self.get_evolution_line(digimon_name))


# Usage example
if __name__ == '__main__':
    # Create service instance
    service = DigimonEvolutionService('../data/digimon_list.xlsx')
    
    # Test with Patamon
    print("\n" + "="*80)
    print("Example: Patamon")
    print("="*80)
    result = service.get_evolution_line('Patamon')
    print(result)
    
    # Test with Agumon
    print("\n" + "="*80)
    print("Example: Agumon")
    print("="*80)
    result = service.get_evolution_line('Agumon')
    print(result)