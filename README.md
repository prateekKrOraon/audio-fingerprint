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

### Error in installing PyAudio in Windows 10

If you face any error in installing PyAudio in Windows 10, follow these instructions.

* Find appropriate `.whl` file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio), for example mine is `PyAudio-0.2.11-cp37-cp37m-win_amd64.whl` and download it.
* Go to the folder where it is downloaded and install the `.whl` file with `pip`:
  ```
  pip install PyAudio-0.2.11-cp37-cp37m-win_amd64.whl
  ```

### Installing ffmpeg

* __For Windows:__
  * Download executables from [here](https://ffmpeg.org/download.html)
  * Add `file_path_to_ffmpeg/bin` to your path variable

* __For Ubuntu:__
  * `sudo apt install ffmpeg`

* __For installing ffmpeg in AWS EC2 instance__
  * Please refer to the following document [here](ffmpeg-installation.md)

## Database Schema and Credentials

Create the following tables.

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