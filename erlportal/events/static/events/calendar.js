const buildCalDay = (dayNum, events=null) => {
    htmlOutput = `<td class='cal-day'><h3 class='day-num'>${dayNum}</h3>`;
    if (events !== null) {
        events.forEach((event) => {
            htmlOutput += `<div class='day-event' style="backgroundColor: ${event.color};"><a class='event-link' href="#${event.slug}"><h4>${event.title}`
        })
    }
};

const buildCalendar = (month, year, events=null) => {
    /*Month is 1 based when passed in. */

    let monthIndex = month - 1;

    const calendar = document.getElementById("calendar-body");
    const prevBtn = document.getElementById('btn-prev-month');
    const nextBtn = document.getElementById('btn-next-month');
    const baseUrl = '/events/calendar';
    let prevMonth = `${year}/${month - 1}`;
    let nextMonth = `${year}/${month + 1}`;
    if (monthIndex === 0) {
        prevMonth = `${year - 1}/12`;
    } else if (monthIndex === 11) {
        nextMonth =  `${year + 1}/1`;
    }

    prevBtn.href = `${baseUrl}/${prevMonth}`;
    nextBtn.href= `${baseUrl}/${nextMonth}`;

    const daysInMonth = new Date(year, monthIndex + 1, 0).getDate();
    const firstWeekday = new Date(year, monthIndex, 1).getDay();
    const lastWeekday = new Date(year, monthIndex, daysInMonth).getDay();
    const dayList = [];


    for (let i = 0; i < firstWeekday; i++) {
        dayList.push('');
    }

    for (let i = 1; i <= daysInMonth; i++) {
        dayList.push(i);
    }

    if (lastWeekday < 6) {
        const trailingDays = 6 - lastWeekday;
        for (let i=0; i < trailingDays; i++) {
            dayList.push('');
        }
    }
    
    let weekDayCount = 0;
    let htmlOutput = '';
    dayList.forEach((item) => {
        if (weekDayCount === 0) {
            htmlOutput += `<tr><td class="cal-day"><div><h3>${item}</h3></div></td>`
            weekDayCount++;
        } else if (weekDayCount === 6) {
            htmlOutput += `<td class="cal-day"><div><h3>${item}</h3></div></td></tr>`
            weekDayCount = 0;
        } else {
            htmlOutput += `<td class="cal-day"><div><h3>${item}</h3></div></td>`;
            weekDayCount++;
        }

    });

    calendar.innerHTML = htmlOutput;


};

const year = parseInt(JSON.parse(document.getElementById('year').textContent));
const month = parseInt(JSON.parse(document.getElementById('month').textContent));
const eventsImport = JSON.parse(document.getElementById('eventsJson').textContent);
events = eventsImport.map(event => {
    return {
        'title': event.title,
        'slug': event.slug,
        'color': event.color,
        'startTime': new Date(event.startTime.slice(0, -1)),
        'endTime': new Date(event.endTime.slice(0, -1)),
    };
});
buildCalendar(month, year, events);