const hexToRgb = (hex) => {
    // Expand shorthand form (e.g. "03F") to full form (e.g. "0033FF")
    const shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
    hex = hex.replace(shorthandRegex, function(m, r, g, b) {
      return r + r + g + g + b + b;
    });
  
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : null;
  };

const getEventTitle = (event) => {
    const url = `/events/event/${event.slug}/`;
    return `<a href='${url}'>${event.title}</a>`;
};

const getEventContent = (event) => {
    return `<div class='date-time'><h4>Start: ${event.startTime.toLocaleString('en-us', {year:'numeric', month: 'long', day:'numeric', hour12: true, hour: 'numeric', minute: '2-digit'})}</h4><h4>End: ${event.endTime.toLocaleString('en-us', {year:'numeric', month: 'long', day:'numeric', hour12: true, hour: 'numeric', minute: '2-digit'})}</h4></div><div class='staffing-summary'><p>Description</p></div>`;
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
            let rgb = hexToRgb(events[i].color);
            htmlOutput += `<div class='day-event event-${gridPos}' style="background-color: rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 0.15); border-color: ${events[i].color};"><a class='event-link' role="button" tabindex="0" data-bs-toggle="popover" data-bs-trigger="focus" data-bs-title="${getEventTitle(events[i])}" data-bs-content="${getEventContent(events[i])}" data-bs-html="true"><h4>${events[i].title}</h4></div>`
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

const paintScreen = () => {
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
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl, {sanitize: false, html: true}));
};

window.addEventListener('load', paintScreen());
