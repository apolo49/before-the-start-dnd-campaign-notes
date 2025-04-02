Solari Date: `INPUT[datePicker:solariDate]`
Gregorian Date: `INPUT[datePicker:gregorianDate]`
<script>
const calendarAPI = Calendarium.getAPI("Solari Calendar");
const currentDate = calendarAPI.getCurrentDate(); // this is an object { year: number, month: number, day: number }

const someOtherCalendarAPI = Calendarium.getAPI("Gregorian Calendar");

console.log(Calendarium.translate(currentDate, calendarAPI, someOtherCalendarAPI));
currentDate
</script>

