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

./ttHbb_preprocess_CSV_file.py
                                 --infile=output.csv               \
                                 --outfile=output_preprocessed.csv
```
