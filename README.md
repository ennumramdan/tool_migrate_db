
# Python Database Migrator - Sync/Backup

Python2.7 script to help you migrate big mysql data

## When you should use it?

Use this tool to migrate / backup your database which has very much data and is difficult to import via phpmyadmin or limitations because you can not access mysql console directly.

## Getting Started

### Prerequisites

1. Install python-dev and python3-dev

```
sudo apt-get install python-dev python3-dev
```

2. Install libmysqlclient

```
sudo apt-get install libmysqlclient-dev
```

### Installing

1. Clone/Download repo

```
git clone https://github.com/ennumramdan/migrate_db_tools.git
```

2. Navigate to the directory

```
cd migrate_db_tools/
```

3. Install the dependencies

```
pip install -r requirements.txt
```

4. Rename and change file config.conf.sample to config.conf

## Usage

### Basic usage[mode]
mode server to client or client to server, this command will migrate all your db

```
1. python2.7 main_db_utility.py -m server_to_client

2. python2.7 main_db_utility.py -m client to_server
```

### More Feature

1. migrate specific table

```
python2.7 main_db_utility.py -m server_to_client -t name_table
```

2. migrate specific table from id a to ...

```
python2.7 main_db_utility.py -m server_to_client -t name_table -id 100
```

3. migrate datas n days back, *request field updated_at in your tables

```
python2.7 main_db_utility.py -m server_to_client -l 7 <-- will migrate datas last 7 days
```



## Authors

* **Muhamad Ramdan** - *Initial work* - [ennumramdan](https://github.com/ennumramdan)
