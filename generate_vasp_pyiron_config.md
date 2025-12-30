
# Instructions to Generate the .pyiron_vasp_config

The `.pyiron_vasp_config` file is essential for configuring the paths to the VASP pseudopotential files (POTCAR files) used in pyiron_workflow's VASP nodes. The file specifies the locations of different VASP potential sets and the default potential set to be used. Below are step-by-step instructions to generate the `.pyiron_vasp_config` file.

## 1. Determine the Locations of Your VASP POTCAR Files

Before creating the `.pyiron_vasp_config` file, ensure that you know the locations of the different POTCAR sets on your system. The common VASP potential directories are `potpaw_64`, `potpaw_54`, and `potpaw_52`, but your setup may vary. The directory structure should look something like this:

```
/home/pyiron_resources_cmmc/vasp/potpaw_64/LDA
/home/pyiron_resources_cmmc/vasp/potpaw_64/GGA
/home/pyiron_resources_cmmc/vasp/potpaw_54/LDA
/home/pyiron_resources_cmmc/vasp/potpaw_54/GGA
/home/pyiron_resources_cmmc/vasp/potpaw_52/LDA
/home/pyiron_resources_cmmc/vasp/potpaw_52/GGA
```

- **LDA** and **GGA** refer to the functional types for the VASP potentials.

## 2. Create the .pyiron_vasp_config File

1. Open a terminal and navigate to your home directory:

    ```bash
    cd ~
    ```

2. Use a text editor (such as `nano` or `vim`) to create and open the `.pyiron_vasp_config` file. For example:

    ```bash
    nano .pyiron_vasp_config
    ```

3. Add the following lines to the file. Make sure to modify the paths according to your setup.

    ```ini
    # Set the default POTCAR set
    # Make sure that the default_POTCAR_set matches one of the suffixes in the vasp_POTCAR_path_*
    default_POTCAR_set = potpaw64
    
    # Path to the root directory containing the VASP pseudopotential files
    pyiron_vasp_resources = /home/pyiron_resources_cmmc/vasp
    
    # Path for different POTPAW versions (adjust these paths according to your setup)
    vasp_POTCAR_path_potpaw64 = {pyiron_vasp_resources}/potpaw_64
    vasp_POTCAR_path_potpaw54 = {pyiron_vasp_resources}/potpaw_54
    vasp_POTCAR_path_potpaw52 = {pyiron_vasp_resources}/potpaw_52
    # Note that pyiron vasp nodes can detect variants of vasp_POTCAR_path_{randomsuffix}
    # So if you want to do something with custom pseudopotentials, you can... 
    # Each of these dirs must have a "GGA" and "LDA" subdirectory structure
    # i.e. 
    # The structure should look like
    # .../vasp/potpaw_64/LDA
    # .../vasp/potpaw_64/GGA
    # .../vasp/potpaw_54/LDA etc.
    ```

4. After you have added the configuration details, save the file:
   - If you're using `nano`, press `Ctrl + O`, then `Enter` to save. Press `Ctrl + X` to exit.
   - If you're using `vim`, press `Esc`, type `:wq`, and press `Enter` to save and exit.

## 3. Verify File Permissions

Ensure that your `.pyiron_vasp_config` file and the POTCAR directories are readable by your user. Run the following command to check the file permissions of the `.pyiron_vasp_config`:

```bash
ls -l ~/.pyiron_vasp_config
```

If necessary, you can modify the permissions to ensure read access:

```bash
chmod 644 ~/.pyiron_vasp_config
```

Also, verify that you have read/copy access to the files inside the VASP resource directories (`potpaw_64`, `potpaw_54`, etc.):

```bash
ls -l /home/pyiron_resources_cmmc/vasp/potpaw_64
```

## 4. Testing Your Configuration

To verify that pyiron is correctly reading the `.pyiron_vasp_config` file, you can either check within your pyiron scripts or write a simple Python script to test the configuration:

```python
import os
from pathlib import Path

# Read the config file
config_file = Path.home().joinpath(".pyiron_vasp_config")
with open(config_file, "r") as f:
    print(f.read())
```

This should print out the contents of your `.pyiron_vasp_config`, and you can check if the paths are correctly generated.

### Additional Notes:
- **Ensure Correct Paths**: Double-check that the paths to your POTCAR directories are correct. Incorrect paths will lead to pyiron not being able to find the necessary POTCAR files for your VASP calculations.

By following these instructions, you'll have a correctly configured `.pyiron_vasp_config` file that points to the appropriate VASP pseudopotential directories.

## 5. Configuring a New Default Pseudopotential Set

The package supports multiple pseudopotential specification CSV files that define which pseudopotential variant to use for each element. By default, the system uses `vasp_pseudopotential_{default_functional}_data.csv` (e.g., `vasp_pseudopotential_GGA_data.csv`). However, you can configure it to use a custom pseudopotential set.

### 5.1. Available Pseudopotential Sets

The package includes several predefined pseudopotential sets:
- `GGA` - Standard GGA pseudopotentials (default if not specified)
- `LDA` - Standard LDA pseudopotentials
- `GGA_MPRelaxSet` - Materials Project RelaxSet GGA pseudopotentials
- `GGA_MatPES` - MatPES GGA pseudopotentials

### 5.2. Configuring a Default Pseudopotential Set

To use a specific pseudopotential set, add the `default_pseudopotential_set` option to your `~/.pyiron_vasp_config` file:

```ini
# Set the default functional (GGA or LDA)
default_functional = GGA

# Set the default pseudopotential set
# This will look for: vasp_pseudopotential_GGA_MPRelaxSet_data.csv
# If not specified, it defaults to: vasp_pseudopotential_GGA_data.csv
default_pseudopotential_set = GGA_MPRelaxSet
```

**Example Configuration:**

```ini
# Set the default POTCAR set
default_POTCAR_set = potpaw64

# Set the default functional
default_functional = GGA

# Set the default pseudopotential specification set
# Options: GGA, LDA, GGA_MPRelaxSet, GGA_MatPES, or any custom set you create
default_pseudopotential_set = GGA_MPRelaxSet

# Path to the root directory containing the VASP pseudopotential files
pyiron_vasp_resources = /home/pyiron_resources_cmmc/vasp

# Path for different POTPAW versions
vasp_POTCAR_path_potpaw64 = {pyiron_vasp_resources}/potpaw_64
vasp_POTCAR_path_potpaw54 = {pyiron_vasp_resources}/potpaw_54
```

**Note:** If `default_pseudopotential_set` is not specified, the system will use `default_functional` (e.g., `GGA` or `LDA`) to construct the CSV filename, maintaining backward compatibility.

## 6. Adding New Pseudopotentials to CSV Files

If you need to add new pseudopotential variants (e.g., `Ba_sv_GW`, `Xe_GW`) that are not present in the existing CSV files, follow these steps:

### 6.1. Locate the CSV File

The pseudopotential specification CSV files are located in:
```
pyiron_workflow_vasp/pyiron_workflow_vasp/vasp_resources/
```

Common files include:
- `vasp_pseudopotential_GGA_data.csv`
- `vasp_pseudopotential_LDA_data.csv`
- `vasp_pseudopotential_GGA_MPRelaxSet_data.csv`
- `vasp_pseudopotential_GGA_MatPES_data.csv`

### 6.2. CSV File Format

Each CSV file has the following columns:
- `potential_name` - The name of the pseudopotential variant (e.g., `Ba_sv`, `Ba_sv_GW`)
- `symbol` - The chemical symbol of the element (e.g., `Ba`, `Xe`)
- `Z` - Atomic number
- `element_name` - Full name of the element
- `n_val_elect` - Number of valence electrons
- `val_elect_config` - Valence electron configuration
- `energy_cutoff_ENMAX` - Energy cutoff (ENMAX) in eV
- `default` - Boolean (`True` or `False`) indicating if this is the default pseudopotential for the element

### 6.3. Adding a New Pseudopotential Entry

To add a new pseudopotential variant (e.g., `Ba_sv_GW`, `Xe_GW`):

1. **Open the CSV file** in a text editor or spreadsheet application.

2. **Find the element section** (e.g., all rows where `symbol == "Ba"`).

3. **Add a new row** with the pseudopotential information. You'll need:
   - The exact `potential_name` as it appears in your POTCAR directory
   - The correct `Z` (atomic number)
   - The `n_val_elect` (number of valence electrons)
   - The `val_elect_config` (valence electron configuration)
   - The `energy_cutoff_ENMAX` (from the POTCAR file header)
   - Set `default` to `True` if this should be the default, or `False` otherwise

4. **Example entries:**

**For `Ba_sv_GW`:**
```csv
potential_name,symbol,Z,element_name,n_val_elect,val_elect_config,energy_cutoff_ENMAX,default
Ba_sv_GW,Ba,56,Barium,10.0,5s2 5p6 5d0.01 6s1.99,187.181,True
```

**For `Xe_GW`:**
```csv
potential_name,symbol,Z,element_name,n_val_elect,val_elect_config,energy_cutoff_ENMAX,default
Xe_GW,Xe,54,Xenon,8.0,5s2 5p6,153.118,True
```

5. **Ensure only one default per element:** For each element, only one pseudopotential should have `default = True`. If you're setting a new variant as default, make sure to set all other variants for that element to `default = False`.

**Note:** If a pseudopotential variant (e.g., `Ba_sv_GW`, `Xe_GW`) is not found in the CSV file when running calculations, you have two options:
- **Option 1:** Add the missing pseudopotential entry to the CSV following the steps above.
- **Option 2:** Use an existing variant as a fallback by setting it as default (e.g., use `Ba_sv` instead of `Ba_sv_GW`).

### 6.4. Finding Pseudopotential Information

To find the required information for a new pseudopotential:

1. **Locate the POTCAR file** in your VASP resources directory:
   ```bash
   ls /path/to/vasp/potpaw_64/GGA/Ba_sv_GW/POTCAR
   ```

2. **Read the POTCAR header** to extract information:
   ```bash
   head -20 /path/to/vasp/potpaw_64/GGA/Ba_sv_GW/POTCAR
   ```
   
   The header typically contains:
   - `ZVAL` - Number of valence electrons
   - `ENMAX` - Energy cutoff
   - Electron configuration information

3. **Compare with existing entries** for the same element to ensure consistency in formatting.

### 6.5. Creating a New Pseudopotential Set CSV

If you want to create an entirely new pseudopotential set (e.g., `GGA_Custom`):

1. **Copy an existing CSV file** as a template:
   ```bash
   cp pyiron_workflow_vasp/pyiron_workflow_vasp/vasp_resources/vasp_pseudopotential_GGA_data.csv \
      pyiron_workflow_vasp/pyiron_workflow_vasp/vasp_resources/vasp_pseudopotential_GGA_Custom_data.csv
   ```

2. **Update the `default` column** for all entries according to your requirements.

3. **Add any new pseudopotential variants** following the steps in Section 6.3.

4. **Configure your `.pyiron_vasp_config`** to use the new set:
   ```ini
   default_pseudopotential_set = GGA_Custom
   ```

### 6.6. Verifying Your Changes

After modifying a CSV file, verify the changes:

```python
import pandas as pd
import csv

csv_path = 'pyiron_workflow_vasp/pyiron_workflow_vasp/vasp_resources/vasp_pseudopotential_GGA_MatPES_data.csv'

# Check defaults for a specific element
with open(csv_path, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['symbol'] == 'Ba':
            print(f"Ba variant: {row['potential_name']}, default: {row['default']}")
```

Or use a simple Python script:

```python
import csv

csv_path = 'path/to/your/csv/file.csv'
element = 'Ba'  # Element to check

with open(csv_path, 'r') as f:
    reader = csv.DictReader(f)
    defaults = [row for row in reader if row['symbol'] == element and row['default'] == 'True']
    print(f"Default pseudopotential for {element}: {defaults[0]['potential_name'] if defaults else 'None found'}")
```

### 6.7. Common Issues

**Issue: Pseudopotential not found**
- **Symptom:** Error message indicating a pseudopotential variant is not found in the CSV.
- **Solution:** Ensure the `potential_name` in the CSV exactly matches the directory name in your POTCAR library (case-sensitive).

**Issue: Multiple defaults for same element**
- **Symptom:** Unexpected behavior when selecting pseudopotentials.
- **Solution:** Ensure only one entry per element has `default = True`. Use a script to verify:
  ```python
  import csv
  from collections import defaultdict
  
  csv_path = 'your_file.csv'
  defaults = defaultdict(list)
  
  with open(csv_path, 'r') as f:
      reader = csv.DictReader(f)
      for row in reader:
          if row['default'] == 'True':
              defaults[row['symbol']].append(row['potential_name'])
  
  # Check for multiple defaults
  for element, variants in defaults.items():
      if len(variants) > 1:
          print(f"WARNING: {element} has multiple defaults: {variants}")
  ```

**Issue: CSV file not being read**
- **Symptom:** System still uses old defaults despite CSV changes.
- **Solution:** 
  - Verify the CSV filename matches the pattern: `vasp_pseudopotential_{default_pseudopotential_set}_data.csv`
  - Check that `default_pseudopotential_set` in your config matches the CSV filename suffix
  - Ensure the CSV file is in the correct location: `pyiron_workflow_vasp/pyiron_workflow_vasp/vasp_resources/`
