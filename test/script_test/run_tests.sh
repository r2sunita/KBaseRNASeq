#!/bin/bash
export KB_RUNTIME=/kb/runtime
export PYTHONPATH="/kb/dev_container/modules/KBaseRNASeq/lib"
python /kb/dev_container/modules/KBaseRNASeq/test/script_test/basic_test.py $1 $2 $3
