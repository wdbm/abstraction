# ttHbb 2017-03

```Bash
rm output.csv
rm output_preprocessed.csv

./ttHbb_ROOT_file_to_CSV_file.py                                   \
                                 --fileroot=output_ttH.root        \
                                 --classlabel=1                    \
                                 --filecsv=output.csv              \
                                 --maxevents=1000                  \
                                 --headings=true

./ttHbb_ROOT_file_to_CSV_file.py                                   \
                                 --fileroot=output_ttbb.root       \
                                 --classlabel=0                    \
                                 --filecsv=output.csv              \
                                 --maxevents=1000                  \
                                 --headings=true

./ttHbb_plots_of_CSV.py                                            \
                                 --infile=output.csv               \
                                 --histogramcomparisons=true       \
                                 --scattermatrix=true

./ttHbb_preprocess_CSV_file.py   --infile=output.csv               \
                                 --outfile=output_preprocessed.csv
```

# ttHbb 2017-04

```Bash
rm data.csv
rm data_preprocessed.csv

filename_ttH="ttH_group.phys-higgs.10205167._000002.out.root"
filename_ttbb="ttbb_group.phys-higgs.10205185._000001.out.root"

./ttHbb_examine_ROOT_file.py     --fileroot="${filename_ttH}"

./ttHbb_ROOT_file_to_CSV_file.py                                     \
                                 --fileroot="${filename_ttH}"        \
                                 --classlabel=1                      \
                                 --filecsv=data.csv                  \
                                 --maxevents=1000                    \
                                 --headings=true

./ttHbb_ROOT_file_to_CSV_file.py                                     \
                                 --fileroot="${filename_ttbb}"       \
                                 --classlabel=0                      \
                                 --filecsv=data.csv                  \
                                 --maxevents=1000                    \
                                 --headings=true

./ttHbb_plots_of_CSV.py                                              \
                                 --infile=data.csv                   \
                                 --histogramcomparisons=true         \
                                 --scattermatrix=true                \
                                 --directoryplots=plots_raw

./ttHbb_preprocess_CSV_file.py   --infile=data.csv                   \
                                 --outfile=data_preprocessed.csv

./ttHbb_plots_of_CSV.py                                              \
                                 --infile=data_preprocessed.csv      \
                                 --histogramcomparisons=true         \
                                 --scattermatrix=true                \
                                 --directoryplots=plots_preprocessed
```
