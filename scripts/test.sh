black src/*.py
python -mpytest test
python -mpytest --doctest-glob="*.py"
read -p "Press any key to resume ..." t