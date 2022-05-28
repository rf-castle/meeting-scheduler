use std::fmt::format;
use chrono::{Date, Datelike, DateTime, Local, NaiveDate, NaiveDateTime, NaiveTime, ParseError, ParseResult, Timelike, TimeZone};
use chrono::format::{parse, Parsed, StrftimeItems};

pub(crate) fn parse_date(content: &str) -> ParseResult<DateTime<Local>> {
    let now = Local::now();
    let mut parsed = Parsed::new();
    parse(&mut parsed, content, StrftimeItems::new("%m/%d %H:%M"))?;
    parsed.set_year(now.year() as i64).ok();
    Ok(
        Local.from_local_datetime(&parsed.to_naive_datetime_with_offset(0)?).unwrap()
    )
}

pub(crate) fn format_date(date: &NaiveDate) -> String{
    let result = date.format("%m/%d");
    result.to_string()
}
pub(crate) fn format_time(date: &NaiveTime) -> String{
    date.format("%H:%M").to_string()
}

pub(crate) fn format_datetime(date: &NaiveDateTime) -> String{
    format!("{} {}", format_date(&date.date()) ,format_time(&date.time()))
}