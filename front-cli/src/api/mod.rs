use chrono::{DateTime, TimeZone};

type DateRange<Tz> = (DateTime<Tz>, DateTime<Tz>);

#[derive(Default, Clone)]
pub(crate) struct FreeDateArgs {

}

pub(crate) trait API{
    // Todo: ログイン
    fn search_reserved_date(&self, company: &str);
    fn check_free_date(&self, args: &FreeDateArgs);
    fn reserve_date<Tz: TimeZone>(&self, company: &str, dates: &[DateRange<Tz>]);
    fn decide_date<Tz: TimeZone>(&self, company: &str, date: DateRange<Tz>);
}