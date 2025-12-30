# pyiron_workflow_vasp

A VASP workflow integration package for pyiron, providing tools and utilities for running and managing VASP calculations within the pyiron workflow framework.

## Installation

The package can be installed using pip:

```bash
# Basic installation
pip install pyiron_workflow_vasp

# Installation with development tools
pip install "pyiron_workflow_vasp[dev]"

# Installation with notebook support
pip install "pyiron_workflow_vasp[notebook]"

# Installation with all optional dependencies
pip install "pyiron_workflow_vasp[dev,notebook]"
```

## Dependencies

The package requires the following core dependencies:
- Python >= 3.8
- numpy >= 1.20.0
- pandas >= 1.3.0
- pymatgen >= 2023.0.0
- pyiron_workflow >= 0.1.0
- ase >= 3.22.0

## Project Information

- **License**: BSD-3-Clause
- **Development Status**: Alpha
- **Documentation**: [GitHub Repository](https://github.com/pyiron/pyiron_workflow_vasp)
- **Bug Tracker**: [GitHub Issues](https://github.com/pyiron/pyiron_workflow_vasp/issues)

## Usage

The package provides a set of tools for running VASP calculations within pyiron workflows. Here's a basic example:

```python
from pyiron_workflow_vasp import vasp

# Create a VASP job
job = vasp.vasp_job(
    structure=your_structure,
    incar_parameters={
        "ENCUT": 400,
        "ISMEAR": 0,
        "SIGMA": 0.1
    }
)

# Run the job
job.run()
```

For more examples, check out the notebooks in the `example_notebooks` directory.

## VASP Configuration

The `.pyiron_vasp_config` file is essential for configuring the paths to the VASP pseudopotential files (POTCAR files) used in pyiron_workflow's VASP nodes. The file specifies the locations of different VASP potential sets and the default potential set to be used.

For detailed configuration instructions, see [generate_vasp_pyiron_config.md](generate_vasp_pyiron_config.md), which includes:
- Basic configuration setup
- Configuring custom pseudopotential sets
- Adding new pseudopotential variants to CSV files

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
