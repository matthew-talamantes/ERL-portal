const getEventStyle = (event) => {
    const underStaffed = 'red';
    const minStaffed = '#ffe300';
    const fullStaffed = 'green';
    if (event.staffNum < event.minSlots) {
        return ` style="border-left: ${underStaffed} solid 5px;"`;
    } else if (event.staffNum < event.slots) {
        return ` style="border-left: ${minStaffed} solid 5px;"`;
    } else if (event.staffNum >= event.slots) {
        return ` style="border-left: ${fullStaffed} solid 5px;"`;
    } else {
        return '';
    }
};

const buildCalDay = (dayNum, events, year, month, today) => {
    const cellDay = new Date(year, month, dayNum);
    if (today.toDateString() === cellDay.toDateString()) {
        htmlOutput = `<td class='cal-day'><div class='day-wrapper today'><h3 class='day-num'>${dayNum}</h3>`;
    } else {
        htmlOutput = `<td class='cal-day'><div class='day-wrapper'><h3 class='day-num'>${dayNum}</h3>`;
    }
    if (events.length > 0) {
        for ( let i = 0; i < events.length; i++) {
            let gridPos = i + 1;
            htmlOutput += `<div class='day-event event-${gridPos}'${getEventStyle(events[i])}><a class='event-link' href="#${events[i].uid}"><h4>${events[i].title}</h4></div>`
        }
    }
    htmlOutput += '</div></td>';
    return htmlOutput;
};

const buildCalendar = (month, year, events=null) => {
    /*Month is 1 based when passed in. */

    let monthIndex = month - 1;
    const today = new Date();
    const calendar = document.getElementById("calendar-body");
    const prevBtn = document.getElementById('btn-prev-month');
    const nextBtn = document.getElementById('btn-next-month');
    const baseUrl = '/shifts/calendar';
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
        dayList.push({'dayNum': '', 'events': []});
    }

    for (let i = 1; i <= daysInMonth; i++) {
        if (events !== null) {
            let dayEvents = [];
            let currentDate = new Date(year, monthIndex, i);
            for (let num = 0; num < events.length; num++) {
                if (((events[num].startTime.getDate() === i && events[num].startTime.getMonth() === monthIndex) || (events[num].endTime.getDate() === i && events[num].endTime.getMonth() === monthIndex)) || (events[num].startTime < currentDate && events[num].endTime > currentDate)) {
                    dayEvents.push(events[num]);
                }
            }
            dayEvents.sort((a, b) => {
                    if (a.startTime < b.startTime) {
                        return -1;
                    }
                    if (a.startTime > b.startTime) {
                        return 1;
                    }

                    return 0;
                });
            dayList.push({'dayNum': i, 'events': dayEvents});
        } else {
            dayList.push({'dayNum': i, 'events': []})
        }
    }

    if (lastWeekday < 6) {
        const trailingDays = 6 - lastWeekday;
        for (let i=0; i < trailingDays; i++) {
            dayList.push({'dayNum': '', 'events': []});
        }
    }
    
    let weekDayCount = 0;
    let htmlOutput = '';
    dayList.forEach((item) => {
        if (weekDayCount === 0) {
            htmlOutput += `<tr>${buildCalDay(item.dayNum, item.events, year, monthIndex, today)}`
            weekDayCount++;
        } else if (weekDayCount === 6) {
            htmlOutput += `${buildCalDay(item.dayNum, item.events, year, monthIndex, today)}</tr>`
            weekDayCount = 0;
        } else {
            htmlOutput += `${buildCalDay(item.dayNum, item.events, year, monthIndex, today)}`;
            weekDayCount++;
        }

    });

    calendar.innerHTML = htmlOutput;


};

const getDateArray = (date) => {
    const dateStrArray = date.split('-');
    let dateArray = dateStrArray.map(item => {
        return parseInt(item);
    });
    dateArray[1] -= 1;
    return dateArray;
};

const getTimeArray = (time) => {
    const timeStrArray = time.split(':');
    const timeArray = timeStrArray.map(item => {
        return parseInt(item);
    });
    return timeArray;
};

const paintScreen = () => {
    const year = parseInt(JSON.parse(document.getElementById('year').textContent));
    const month = parseInt(JSON.parse(document.getElementById('month').textContent));
    const eventsImport = JSON.parse(document.getElementById('eventsJson').textContent);
    events = eventsImport.map(event => {
        const dateArray = getDateArray(event.date);
        const startTimeArray = getTimeArray(event.startTime);
        const endTimeArray = getTimeArray(event.endTime);
    return {
        'title': event.title,
        'slug': event.slug,
        'uid': event.uid,
        'date': new Date(dateArray[0], dateArray[1], dateArray[2]),
        'startTime': new Date(dateArray[0], dateArray[1], dateArray[2], startTimeArray[0], startTimeArray[1], startTimeArray[2]),
        'endTime': new Date(dateArray[0], dateArray[1], dateArray[2], endTimeArray[0], endTimeArray[1], endTimeArray[2]),
        'minSlots': event.minSlots,
        'slots': event.slots,
        'staffNum': event.staffNum
    };
    });
    buildCalendar(month, year, events);
};

window.addEventListener('load', paintScreen());
