#!/bin/bash

projectName="abstraction"

pyreverse -my -A -o png -p "${projectName}" **.py
sfood . | sfood-graph | dot -Tpdf > "${projectName}"_graph.pdf
convert -density 1000 "${projectName}"_graph.pdf "${projectName}"_graph.png
rm "${projectName}"_graph.pdf
