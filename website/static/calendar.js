
function consoleInit(deadline_list) {
        // deadline list: odd indices -> title, even indices -> dates
		var deadlineList = [];
		for (var d in deadline_list ) {
			deadlineList.push(deadline_list[d]);
		};

        document.addEventListener('DOMContentLoaded', function() {
			var calendarEl = document.getElementById('calendar');
			var calendar = new FullCalendar.Calendar(calendarEl, {
				initialView: 'dayGridMonth'
			});
			
			for (var i = 2; i < deadlineList.length;) {
				calendar.addEvent({
					title: deadlineList[i],
					start: deadlineList[i - 1],
					end: deadlineList[i + 1],
				});
				i += 2;
                
			}
			calendar.render();
		});
}
