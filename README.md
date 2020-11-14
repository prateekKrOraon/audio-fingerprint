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
## License

    MIT License

    Copyright (c) 2020 Prateek Kumar Oraon
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.