**CS319 Fall 2022-23**
**Section 2**

*Group Members:*
\
Bora Yılmaz - 22003359\
Cengizhan Terzioğlu - 22003014\
Emirkan Derköken - 22002693\
Göktuğ Kuşcu - 22002867\
Murat Güney Kemal - 22002692\
Onur Asım İlhan - 21903375

**Erasmus/Bilateral Exchange Application**

Students will have the ability to apply Erasmus directly through this application. The application will eliminate the stress of formality and the anxiety that getting lost in lengthy guidelines causes. Basically, the website will lead the students throughout the whole application & post-Erasmus process bit-by-bit in a simple manner as well as helping students shape their application list by showing where students with similar academic standings were placed the preceding years and guiding them with preparing their schedules.

The application’s main goal on the staff’s end is to minimize the paperwork and manual labor. The application will also guide the staff users throughout the process by listing and scheduling the work that awaits them at any moment in order to reduce the mental load of sketching and planning.

The main objective of our project is to create a new and improved website for Bilkent Engineering Faculty’s Erasmus/Exchange program. React will be used for the frontend part of the project and Django will be used as the backend part of the project. The database system has not been decided.

*Student* related features:
- Access the list of available partner universities of his department.
- Check frequently asked questions page specific to their departments.
- Create a partner university preference list from listed universities.
- Receive suggestions regarding the best fit partner university according to the student’s erasmus score.
- Fill and send the erasmus application form through the app.
- Access the previously matched and accepted courses of the partner university.
- Keep track of the status of the sent erasmus application.
- Receive suggestions for sample schedules that can be prepared based on the student’s remaining course load and the proposed courses by the partner university
- Select and send the proposed courses and their syllabuses through the app.
- Cancel the erasmus application (Keep track of cancellation deadline),
- Upload his transcript (and possibly course projects) after the exchange program is over.

*Staff* related features
- View all students’ applications and each application’s status.
- Check frequently asked questions page specific to their departments.

*Exchange Coordinator* (extends staff) related features:
- Evaluate and approve/reject the applications through the app.
- Modify frequently asked questions page specific to their departments.
- Automatically match the students with the partner universities.
- Automatically send verification requests to the matched students.
- Get a notification (or a mail) in the case of a cancellation.
- Sign the documents virtually.
- Check a student’s transcript (and possibly course projects) at the exchange application’s last stage.

*Course Coordinator* (extends staff) related features:
- Approve or decline the proposed courses through the application.
- Update the existing course-list if there is a new entry.

*Chair* (extends staff) related features:
- Approve/reject and upload/modify documents and requests.
