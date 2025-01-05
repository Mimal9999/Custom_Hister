<h1>Custom Hister - Fan Project</h1>

<p><strong>Custom Hister</strong> is a fan-made project that allows you to play the <em>Hister</em> game using custom cards with your own songs from YouTube. The name is Hister, not to use the original name, just in case. The project includes an Android app that works similarly to the original, as well as a set of tools to create your own cards based on YouTube playlists.</p>

<h2>Required Tools:</h2>
<ul>
    <li>Python 3.13.1</li>
    <li>Libraries installed from the <code>requirements.txt</code> file</li>
    <li>Visual Studio with MAUI (for editing card designs)</li>
</ul>

<h2>Download:</h2>
<p>You can download the executable files here:</p>
<ul>
    <li><a href="master/Executable/com.companyname.customhister-Signed.apk" download="download">CustomHister</a> - Android application</li>
    <li><a href="https://github.com/Mimal9999/Custom_Hister/blob/master/Executables/CardsGenerator.rar">CardsGenerator</a> - Card generation application</li>
    <li><a href="https://github.com/Mimal9999/Custom_Hister/blob/master/Executables/PythonScripts.rar">PythonScripts</a> - Python scripts for data generation</li>
</ul>
<p>You can also build the applications yourself by cloning the repository.</p>

<p>All files have been scanned using VirusTotal. The <code>CardsGenerator.rar</code> file was flagged by 1 out of 62 services as suspicious, likely due to the lack of a digital signature for the Windows application. If you do not trust the <code>.exe</code> application, you can build it yourself by cloning the repository available <a href="https://github.com/Mimal9999/CardsGenerator">HERE</a>.</p>

<h2>Tool Usage Guide:</h2>

<h3>1. Create Custom Game Cards</h3>

<p>To create your own cards for the game, you need to prepare a playlist on YouTube. The playlist can be set to public or private. If the playlist contains songs that require signing into YouTube, you will need to open a browser and log into YouTube while the script is running.</p>

<p><strong>All Python scripts can be found in the <code>Hister/PythonScripts</code> folder.</strong></p>

<h4>Step 1: Run <code>PlaylistToExcel.py</code></h4>

<p>In the first step, run the script <code>PlaylistToExcel.py</code> via the terminal. Open the terminal in the directory where the script is located and enter the following command:</p>

<pre><code>python PlaylistToExcel.py</code></pre>

<p>Then paste the link to the YouTube playlist and press Enter. Afterward, provide the name of the person who added the playlist. This is not required, but it’s nice to know which of your friends added the song.</p>

<p>The script will run for a few minutes, depending on the number of songs in the playlist. Once the script finishes, a file named <code>playlist_data.xlsx</code> will be created.</p>

<h4>Step 2: Run <code>filter.py</code></h4>

<p>Next, run the <code>filter.py</code> script in the same way as before. The script will select the artist, song title, and other data from the playlist. It will also filter the song titles, attempting to remove the artist’s name from the title and eliminating common, unnecessary phrases like "Official Music Video," etc. If you wish, you can manually adjust all the data in this file.</p>

<h4>Step 3: Run <code>joinExcelData.py</code></h4>

<p>Afterward, run the <code>joinExcelData.py</code> script in the same manner as the previous scripts.</p>

<h3>2. Handling Multiple Playlists</h3>

<p>If each of your friends has sent you their own playlist, repeat these steps for each playlist, changing the output and input file names, and editing the <code>.py</code> scripts using a text editor (e.g., Notepad). You will need to modify the following lines:</p>

<p>For the <code>PlaylistToExcel.py</code> file:</p>
<pre><code>def save_to_excel(data, filename='playlist_data.xlsx'): </code></pre>
<p>Change the filename to a different name.</p>

<p>For the <code>filter.py</code> file:</p>
<pre><code>input_excel = 'playlist_data.xlsx'  # Path to the input Excel file
output_excel = 'filtered_data.xlsx'  # Path to the output Excel file</code></pre>
<p>Also, change the filenames to others.</p>

<h3>3. Merging Data</h3>

<p>Once you have all the <code>filtered_data.xlsx</code> files, place them in the <code>ExcelFiles</code> folder.</p>

<p>Next, run the <code>joinExcelData.py</code> script again. This script will merge all the files into one large file and remove any duplicate links. Keep in mind that some songs might have been uploaded to YouTube by different channels or under different names, meaning the link may not be the same and such duplicates will not be removed.</p>

<h3>4. Final Steps</h3>

<p>Once you have the final <code>merged_excel_cleaned.xlsx</code> file, use the <code>ExcelToJson.py</code> script to generate the <code>output.json</code> file.</p>

<p>With the <code>output.json</code> file in hand, run the <strong>CardsGenerator</strong> app. You can find the app in the GitHub repository under this <a href="https://github.com/Mimal9999/CardsGenerator">link</a>.</p>

<p>Select the <code>output.json</code> file in the app and specify where to save the <code>.pdf</code> file for printing the cards. Then, generate the cards. This may take a few minutes, depending on the number of cards to be generated.</p>

<h3>5. Adjusting Printing Settings</h3>

<p>If the generated <code>.pdf</code> file doesn’t print well on your printer, you may need to adjust certain settings in the code to better suit your printer. If you want, you can also adjust the appearance of the cards by editing the controls in the app.</p>

<h2>Attribution of Used Images:</h2>
<ul>
    <li>www.freepik.com</li>
    <li><a href="https://www.vecteezy.com/free-png/audio-visualizer">Audio Visualizer PNGs by Vecteezy</a></li>
</ul>
