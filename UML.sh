#!/bin/bash

project_name="abstraction"

pyreverse -my -A -o png -p "${project_name}" **.py
sfood . | sfood-graph | dot -Tpdf > "${project_name}"_graph.pdf
convert -density 1000 "${project_name}"_graph.pdf "${project_name}"_graph.png
rm "${project_name}"_graph.pdf
