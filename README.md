# mvbcoins - A Minimally Viable Blockchain
<h2>Actionables</h2>
<ul>
  <li>Refactor code for server/node by encapsulating operations using a class</li>
</ul>

<h3>Step-by-step process to building and running the executable</h3>
<p style="color:red;">This software project assumes you have python 3.x installed on your
system.</p>
  1. Install "pyinstaller" by running the following command from your
  command-line interface ==> ```pip install pyinstaller```
  2. Build the project from the root directory ==> ```make build```
  3. Run the executable with the proper arguments. (Note: port & peers are just examples here) ==> 
  ```./node --port 9182 --peers 9034,9872,8990,8024,9011```
  4. Begin transactions
