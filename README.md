# Song Identification

An application which detects songs based on existing audio fingerprints stored in a database.

## Technology used

* Python
* AWS for hosting
* Flutter application for client side

## Requirements

### Prerequisites for pyaudio

For Linux distributions install these files in the following order.

* [libxml++](https://pkgs.org/search/?q=libxml%2B%2B)
* [libffado](https://pkgs.org/search/?q=libffado)
* [glibc](https://pkgs.org/download/glibc) (If not already installed)
* [glibc-devel](https://pkgs.org/download/glibc-devel) (If not already installed)
* [libjack](https://pkgs.org/download/libjack)
* [portaudio](https://pkgs.org/search/?q=portaudio)
* [portaudio-devel](https://pkgs.org/search/?q=portaudio-devel)

After installing the above files run the following command

    pip install -r requirements.txt

### Installing ffmpeg

Please refer to the following document [here](ffmpeg-installation.md)

## Database Schema and Credentials

Create the following tables

```sql
CREATE TABLE
    songs(
        id INT(11) AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(256) NOT NULL,
        artist VARCHAR(256) NOT NULL,
        album VARCHAR(256) NOT NULL
    ) ENGINE=INNODB;
```

```sql
CREATE TABLE
    fingerprints(
        song_id INT(11) NOT NULL,
        hash VARCHAR(256) NOT NULL,
        offset INT(11) NOT NULL,
        CONSTRAINT song_index FOREIGN KEY (song_id)
        REFERENCES songs(id)
    ) ENGINE=INNODB;
```

For database credentials create a file `cred.yaml`

```yaml
mysql_host: 'host_address'
mysql_user: 'admin_username'
mysql_password: 'admin_password'
mysql_db: 'database_name'
mysql_port: 'port_number'
```