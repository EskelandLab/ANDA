# Directory with scripts
$scriptsDir = (Get-Location).Path
# Read parameters from pipeline_parameters.txt
$pipelineParams = Get-Content -Path "${scriptsDir}\pipeline_parameters.txt"
$dirName = $pipelineParams[0]
$imagejPath = $pipelineParams[1]
$outlines = $pipelineParams[9]

# Change to the directory specified in $dirName
Set-Location -Path $dirName
Get-ChildItem | Where-Object { $_.Extension -eq ".tif" } | Select-Object -ExpandProperty Name | Out-File -FilePath "file_names.txt"

# Change back to the original directory
Set-Location -Path $scriptsDir

# Make directories to store results
$dirsLen = $null  # It seems like $dirsLen is not being used in your script, so I'm assigning it a null value.
mkdir "${dirName}_results_cells"
mkdir "${dirName}_results_neurites"
mkdir "${dirName}_results_branching"
if ($outlines -eq "save_outlines") {
    mkdir "${dirName}_outlines_cells"
    mkdir "${dirName}_outlines_neurites"
    mkdir "${dirName}_outlines_branching"
}

# Run ImageJ and Python scripts
& "${imagejPath}\ImageJ-win64.exe" --ij2 --headless --run "${scriptsDir}\cell_metrics.py"
python data_sort.py
