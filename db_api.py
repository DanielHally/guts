from dataclasses import dataclass
import mysql.connector
from mysql.connector.constants import ClientFlag

@dataclass
class User:
    """Higher level representation of a user (read-only)"""

    id: int
    username: str
    email: str
    password: str
    cityCode: int

@dataclass
class Website:
    """Higher level representaiton of a website (read-only)"""

    id: int
    name: str
    countryCode: int
    link: str
    isHomepage: bool

class DatabaseAccessor:
    def __init__(self):
        # Connect to database
        self._db = mysql.connector.connect(
            host="[REDACTED]",
            user="root",
            password="",
            client_flags=[ClientFlag.SSL],
            ssl_ca="ssl/server-ca.pem",
            ssl_cert="ssl/client-cert.pem",
            ssl_key="ssl/client-key.pem",
            database="GlobalTouch_2"
        )

    def _bool_to_int(self, val: bool):
        return 1 if val else 0

    def _commit_query(self, query: str):
        """Private - Runs an SQL query and commits it"""

        # Create temporary connection
        cursor = self._db.cursor()

        # Run query
        cursor.execute(query)

        # Commit results
        self._db.commit()
    
    def _get_query(self, query: str):
        """Private - Runs an SQL query and returns the results"""

        # Create temporary connection
        cursor = self._db.cursor()

        # Run query
        cursor.execute(query)

        # Return results
        return cursor.fetchall()

    def _clear_table(self, table: str):
        """Public - deletes all rows in a table
        (For manual use, probably not needed in program)"""
        self._commit_query(f"DELETE FROM {table}")
    
    #########
    # Users #
    #########

    def add_user(self, username: str, password: str, email: str, city_name: str, country_name: str):
        """Public - Adds a user to the database
        Creates the city and country if needed"""

        # Insert user into database
        city_code = self.city_name_to_code(city_name, country_name)
        self._commit_query(f"""
            INSERT INTO user (username, password, email, cityCode)
            VALUES ("{username}", "{password}", "{email}", "{city_code}")
        """)

    def get_user_by_name(self, username: str):
        """Public - Gets a user by their username
        Returns None if they don't exist"""

        # Try get user
        ret = self._get_query(f"""
            SELECT userID, username, email, password, cityCode
            FROM user
            WHERE username = "{username}"
        """)

        if len(ret) > 0:
            # Convert result to class and return
            return User(*ret[0])
        else:
            # Not found
            return None
        
    def check_login(self, username: str, password: str):
        """Public - Tries to log in as a user, returns whether it succeeds
        (Not actually secure at all, plaintext & client side, just for illustration)"""

        # Try get user
        user = self.get_user_by_name(username)

        # Make sure user exists
        if user is None:
            return False
        
        # Check password
        return user.password == password
    
    #############
    # Countries #
    #############

    def _add_country(self, country_name: str):
        """Private - Creates a new country"""

        # Insert country into database
        self._commit_query(f"""
            INSERT INTO country (countryName)
            VALUES ("{country_name}")
        """)
    
    def _get_country_code(self, name: str):
        """Private - Gets all country codes matching a name"""

        # Get matching countries
        return self._get_query(f"""
            SELECT countryCode FROM country
            WHERE countryName = "{name}"
        """)
    
    def _get_country_name(self, code: str):
        """Private - Gets all country names matching a code"""

        # Get matching countries
        return self._get_query(f"""
            SELECT countryName FROM country
            WHERE countryCode = {code}
        """)
    
    def country_name_to_code(self, name: str):
        """Public - Gets the code for a country by name
        Creates the country if it doesn't exist"""

        # Try get the country
        ret = self._get_country_code(name)

        # Check success
        if len(ret) > 0:
            # Return code
            return ret[0][0]
        else:
            # Create it if it doesn't exist
            self._add_country(name)

            # Return new code
            return self._get_country_code(name)[0][0]

    def country_code_to_name(self, code: int):
        """Public - Gets the name of a country from its code"""

        # Get country and return name
        return self._get_country_name(code)[0][0]
    
    def get_all_countries(self):
        """Public - Gets all country names"""

        # Get all countries
        ret = self._get_query("""
            SELECT countryName
            FROM country
        """)

        # Unpack 1-item lists
        return [x[0] for x in ret]
    
    def rename_country(self, old: str, new: str):
        """Public - Renames a country
        (For manual use, probably not needed in program)"""

        # Update name
        self._commit_query(f"""
            UPDATE country
            SET countryName = "{new}"
            WHERE countryName = "{old}"
        """)
    
    ##########
    # Cities #
    ##########

    def _add_city(self, city_name: str, country_code: int):
        """Private - Creates a new city"""

        # Insert city into database
        self._commit_query(f"""
            INSERT INTO city (cityName, countryCode)
            VALUES ("{city_name}", {country_code})
        """)

    def _get_city_by_name(self, name: str):
        """Private - Gets all cities matching a name"""

        # Get matching cities
        return self._get_query(f"""
            SELECT cityCode, cityName, countryCode FROM city
            WHERE cityName = "{name}"
        """)
    
    def _get_city_by_code(self, code: str):
        """Private - Gets all cities matching a code"""

        # Get matching cities
        return self._get_query(f"""
            SELECT cityCode, cityName, countryCode FROM city
            WHERE cityCode = {code}
        """)

    def city_name_to_code(self, name: str, country_name: str):
        """Public - Gets the code for a city by name
        Creates the city if it doesn't exist
        Requires country name in case city needs to be created"""

        # Try get the city
        ret = self._get_city_by_name(name) # [(cityCode, cityName, countryCode)]

        # Check success
        if len(ret) > 0:
            # Return code
            return ret[0][0]
        else:
            # Create it if it doesn't exist
            country_code = self.country_name_to_code(country_name)
            self._add_city(name, country_code)

            # Return new code
            return self._get_city_by_name(name)[0][0]


    def city_code_to_name(self, code: int):
        """Public - Gets the name of a city from its code"""

        # Get the city and return name
        return self._get_city_by_code(code)[0][1]

    def get_all_cities(self):
        """Public - Gets all city names"""

        # Get all cities
        ret = self._get_query("""
            SELECT cityName
            FROM city
        """)

        # Unpack 1-item lists
        return [x[0] for x in ret]
    
    def city_name_to_country_name(self, city_name: str):
        """Public - Takes a city name and returns the name of the country it's in"""

        # Get country code
        country_code = self._get_query(f"""
            SELECT countryCode
            FROM city
            WHERE cityName = "{city_name}"
        """)[0][0]

        # Return country name
        return self.country_code_to_name(country_code)

    def city_code_to_country_name(self, code: int):
        """Public - Takes a city code and returns the name of the country it's in"""

        # Get country code
        country_code = self._get_query(f"""
            SELECT countryCode
            FROM city
            WHERE cityCode = "{code}"
        """)[0][0]

        # Return country name
        return self.country_code_to_name(country_code)

    ############
    # Websites #
    ############

    def add_website(self, name: str, is_homepage: bool, link: str, country_name: str):
        """Public - Creates a website
        Creates the country if needed"""

        # Convert to int for SQL
        is_homepage = self._bool_to_int(is_homepage)

        # Insert website into database
        country_code = self.country_name_to_code(country_name)
        self._commit_query(f"""
            INSERT INTO website (name, isHomepage, link, countryCode)
            VALUES ("{name}", "{is_homepage}", "{link}", {country_code})
        """)

    def get_websites_from_other_countries(self, country_name: str, get_homepages: bool):
        """Public - Gets all websites shown to a country
        (In other words, all websites from countries other than the one given)"""

        # Convert to int for SQL
        get_homepages = self._bool_to_int(get_homepages)

        # Get country code
        code = self.country_name_to_code(country_name)

        # Get websites from other countries
        ret = self._get_query(f"""
            SELECT websiteID, name, countryCode, link, isHomepage
            FROM website
            WHERE countryCode != {code}
            AND isHomepage = {get_homepages}
        """)

        # Parse results
        return [Website(*w) for w in ret]

    def get_websites_from_country(self, country_name: str, get_homepages: bool):
        """Public - Gets all websites from a country"""

        # Convert to int for SQL
        get_homepages = self._bool_to_int(get_homepages)

        # Get country code
        code = self.country_name_to_code(country_name)

        # Get websites from a country
        ret = self._get_query(f"""
            SELECT websiteID, name, countryCode, link, isHomepage
            FROM website
            WHERE countryCode = {code}
            AND isHomepage = {get_homepages}
        """)

        # Parse results
        return [Website(*w) for w in ret]
