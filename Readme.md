# IDS for Authentication Services

IDS for authentication services is primarily made up of two simulations:

 - Intrusion Detection System Simulation: The IDS blocks requests based on written rules.
 - Attack Simulation: Various attacks such as horizontal and vertical attacks are simulated. 

# IDS Simulation

The IDS simulation consists of a flask server, redis and SQLite3.

 - Flask Server: The flask server has RESTful API endpoints which can be used for authentication. localhost:5000/authenticate is the endpoint used for authentication. The endpoint only supports POST request. It requires the body as follows:

> {"user": username, 
"password": password, 
"metadata": 
{"ip": ip_address,
 "cookie" : true,
 "redirect":true
 "UserAgent": {
 "os": os_version,
 "browser" : browser_version
 }}}

 - Redis Server: Redis server is used to quickly fetch information to execute intrusion rules. 
 - SQLite3: Stores legitimate user, password information.

# Attack Simulation

Attack simulation consists of two types of attacks. The first type is targeted attack and is specific to a user. While, the second type of attack targets a wide range of users.

# Setting up the project

 - First bring up the Redis Server: Requires installation of redis server. Later, bring up the redis server as follows: 

> redis-server /usr/local/etc/redis.conf
 - Initialize the authenticate user-password pairs: 
> Run Utils/PreProcess/PreProcess.py to update the user password pairs and leaked password information as well.
 - Important files are as follows:
> LEAKED_DATA_UPDATED - $U_A$ - The username, password pair available to an attacker.
> LEGITIMATE_USER_DATA - $U_L$ - The list of legitimate user, passwords.
> LEAKED_LEGITIMATE_USERS - $x*U_L$ - x percent of legitimate users are leaked.
> LEAKED_LEGITIMATE_PASSWORDS - Some passwords are leaked as well.
 - Creating the SQLite3 database:
> Run Utils/SqliteDBCreator
 - Populate the SQLite database:
> Run Utils/SqliteDBPopulator
 - Bring up the flask server:
> pipenv shell in Simulation/IDSSimulation folder and run flask as 'flask run'
 - Different attacks can be carried out. Some attacks which are simulated are password tweaking, password stuffing and commonly used password attacks.
 - Stat info about the leaked password can be analyzed from: 
 > Utils/UserPasswordStats