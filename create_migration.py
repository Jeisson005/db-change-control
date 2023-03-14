import os

folder = 'files'
enc = 'utf-16-le'
ignore = ['User'] + ['Table','Schema','Database']
drop = ['PROCEDURE','FUNCTION','TYPE','VIEW']
replace = ['StoredProcedure','UserDefinedFunction','UserDefinedTableType','View']

files = os.listdir(folder)

for file in files:
    print(file)
    rm = False
    for i in ignore:
        if file.endswith(f'.{i}.sql'):
            os.remove(os.path.join(folder,file))
            rm = True
            break
    if rm:
        continue
    with open(os.path.join(folder,file), 'r', encoding=enc) as fin:
        data = fin.read()
        for d in drop:
            data = data.replace(f'DROP {d} ',f'DROP {d} IF EXISTS ')
        data = data.splitlines(True)
        data = filter(lambda line: ' Script Date: ' not in line, data[2:])
    with open(os.path.join(folder,file), 'w') as fout:
        fout.writelines(data)
    for r in replace:
        if file.endswith(f'.{r}.sql'):
            migration = file.replace('dbo.','R__')
            migration = migration.replace(f'.{r}.',f'_{r}.')
            os.rename(os.path.join(folder,file),os.path.join(folder,migration))
            break
