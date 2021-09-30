import os
import subprocess
import tarfile

# This deals with getting all the identifiers from the project files. It ignores comments by avoiding lines with
# common comment symbols. The words are then added to a list (avoiding any duplicates) and sorted alphabetically.
def getWords(currentProject, directory):
    Identifiers = list()

    os.chdir(directory)
    for root, subdirs, files in os.walk(directory):
        for project in files:
            if project == currentProject:
                with open(os.path.join(root, currentProject), 'r'):
                    for line in open(os.path.join(root, project)):
                        if not line.startswith('%') and not line.startswith('//') and not line.startswith('#'):
                            words = line.split(" ")
                            for word in words:
                                if Identifiers.__contains__(word) is False and (len(word) >= 3):
                                    Identifiers.append(word)
    return sorted(Identifiers)

# This deals with creating the other html pages for each project. The pages display the file name, total number of lines
# in the file, and the associated identifiers gathered earlier.
def generateProjectPages(projectList):
    for project in projectList:

        # Creating the idList allowed the identifiers to be displayed in a less cluttered fashion.
        idList = ""
        for identifier in project['identifiers']:
            id = "<li> " + identifier + " </li>"
            idList = idList + id

        if project["name"].endswith('.c'):
            cHtml = open('summary_a1.html', 'w')
            message = """
            <!DOCTYPE html>
            <html>
               <body>
                            <h1>Thomas Kressman's CSC344 Work Page</h1>
                            <h2>Project 1 - C</h2>
                  <ul>
                  <li><b>File Name:</b> """ + str(project["name"]) + """</li>   
                  <li><b>Line Count:</b> """ + str(project["line_count"]) + """</l1>  
                  <h3>Identifiers:</h3> """ + idList + """ 
                  </ul>
               </body>
            </html>"""
            cHtml.write(message)
            cHtml.close()

        if project["name"].endswith('.clj'):
            clojureHtml = open('summary_a2.html', 'w')
            message = """
            <!DOCTYPE html>
            <html>
               <body>
                            <h1>Thomas Kressman's CSC344 Work Page</h1>
                            <h2>Project 2 - Clojure</h2>
                  <ul>
                  <li><b>File Name:</b> """ + str(project["name"]) + """</li>   
                  <li><b>Line Count:</b> """ + str(project["line_count"]) + """</l1>  
                  <h3>Identifiers:</h3> """ + idList + """ 
                  </ul>
               </body>
            </html>"""
            clojureHtml.write(message)
            clojureHtml.close()

        if project["name"].endswith('.scala'):
            scalaHtml = open('summary_a3.html', 'w')
            message = """
            <!DOCTYPE html>
            <html>
               <body>
                            <h1>Thomas Kressman's CSC344 Work Page</h1>
                            <h2>Project 3 - Scala</h2>
                  <ul>
                  <li><b>File Name:</b> """ + str(project["name"]) + """</li>   
                  <li><b>Line Count:</b> """ + str(project["line_count"]) + """</l1>  
                  <h3>Identifiers:</h3> """ + idList + """ 
                  </ul>
               </body>
            </html>"""
            scalaHtml.write(message)
            scalaHtml.close()

        if project["name"].endswith('.pl'):
            prologHtml = open('summary_a4.html', 'w')
            message = """
            <!DOCTYPE html>
            <html>
               <body>
                            <h1>Thomas Kressman's CSC344 Work Page</h1>
                            <h2>Project 4 - Prolog</h2>
                  <ul>
                  <li><b>File Name:</b> """ + str(project["name"]) + """</li>   
                  <li><b>Line Count:</b> """ + str(project["line_count"]) + """</l1>  
                  <h3>Identifiers:</h3> """ + idList + """ 
                  </ul>
               </body>
            </html>"""
            prologHtml.write(message)
            prologHtml.close()

        if project["name"].endswith('.py'):
            pythonHtml = open('summary_a5.html', 'w')
            message = """
            <!DOCTYPE html>
            <html>
               <body>
                            <h1>Thomas Kressman's CSC344 Work Page</h1>
                            <h2>Project 5 - Python</h2>
                  <ul>
                  <li><b>File Name:</b> """ + str(project["name"]) + """</li>   
                  <li><b>Line Count:</b> """ + str(project["line_count"]) + """</l1>  
                  <li><h3>Identifiers:</h3></li> """ + idList + """ 
                  </ul>
               </body>
            </html>"""
            pythonHtml.write(message)
            pythonHtml.close()

# Creates the index page where all projects are displayed.
def generateIndexPage():
    html = open('index.html', 'w')
    message = """
    <html>
       <head>
       <title>CSC 344 Project Summarization</title>
       </head>
       <body>
                    <h1>Thomas Kressman's CSC344 Work Page</h1>
                    <h2>This is a summarization of my work done during the Spring 2021 semester.</h2>
          <ul>
          <li><a href="summary_a1.html">C Project</a> - Auto-Complete Suggestions</li>   
          <li><a href="summary_a2.html">Clojure Project</a> - Symbolic Simplification</l1>  
          <li><a href="summary_a3.html">Scala Project</a> - Pattern Matcher</li>
          <li><a href="summary_a4.html">Prolog Project</a> - Social Distancing Simulator</li>    
          <li><a href="summary_a5.html">Python Project</a> - Automated Assignment Summarizer and Emailer</li>
          </ul>
       </body>
    </html>"""
    html.write(message)
    html.close()


# The main function focuses on gathering the files from the directory supplied, getting some data on those files,
# and putting it all into a list where they can be accessed later.
def main():
    directory = input("Enter folder directory: ")
    projectList = []
    for root, subdirs, files in os.walk(directory):
        for project in files:
            if project.endswith(('.c', '.clj', '.scala', '.pl', '.py')):
                lineCount = subprocess.check_output(['wc', '-l', os.path.join(root, project)])
                words = getWords(project, directory)
                # projectInfo is a dictionary which was used to store various data about each indiviual project.
                # This made it easier to create html pages for each project.
                projectInfo = {'name': project,
                               'line_count': str(lineCount[0:3]),
                               'identifiers': words}
                projectList.append(projectInfo)

    generateIndexPage()
    generateProjectPages(projectList)


main()

# Creates the tar file containing all the projects and the html pages.
fileName = 'CSC344_Summary.tar.gz'
tar = tarfile.open(fileName, 'w:gz')
tar.add("./")
tar.close()

# Sends the email to the given address along with the tar file.
sendTo = input("What email would you like to send the file to?")
print("Sending tar file via email to: " + sendTo)
email = subprocess.Popen('mutt -s "CSC344 Python Project - Thomas Kressman" ' + sendTo + ' -a ' + fileName + ' ', shell=True)
email.communicate()