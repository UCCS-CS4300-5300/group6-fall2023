sprint_num=4
python -m pylint popularity_assessor > sprint${sprint_num}_pylint.txt
python -m coverage run manage.py test
python -m coverage report > sprint${sprint_num}_coverage.txt
python -m radon cc popularity_assessor > sprint${sprint_num}_cc.txt
python -m radon cc -a -s popularity_assessor > sprint${sprint_num}_abc.txt
python -m radon mi -i A popularity_assessor > sprint${sprint_num}_mi.txt
python -m radon hal popularity_assessor > sprint${sprint_num}_hal.txt
python -m radon raw popularity_assessor > sprint${sprint_num}_loc.txt