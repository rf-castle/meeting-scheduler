use chrono::{DateTime, TimeZone, Utc};
use reqwest::Result;

const ENDPOINT: &str = "";

type DateRange<Tz> = (DateTime<Tz>, DateTime<Tz>);

#[derive(Default, Clone)]
pub struct FreeDateArgs {

}

pub trait API{
    // Todo: ログイン
    fn search_reserved_date(&self, company: &str) -> Result<()>;
    fn check_free_date(&self, args: &FreeDateArgs) -> Result<Vec<DateRange<Utc>>>;
    fn reserve_date<Tz: TimeZone>(&self, company: &str, dates: &[DateRange<Tz>]) -> Result<()>;
    fn decide_date<Tz: TimeZone>(&self, company: &str, date: &DateRange<Tz>) -> Result<()>;
}
pub struct APIImpl{

}

impl APIImpl{
    pub fn new() -> Self{
        APIImpl{}
    }
}

impl API for APIImpl {

    fn search_reserved_date(&self, company: &str) -> Result<()> {
        Ok(())
    }

    fn check_free_date(&self, args: &FreeDateArgs) -> Result<Vec<DateRange<Utc>>> {
        Ok(vec![])
    }

    fn reserve_date<Tz: TimeZone>(&self, company: &str, dates: &[DateRange<Tz>]) -> Result<()> {
        Ok(())
    }

    fn decide_date<Tz: TimeZone>(&self, company: &str, date: &DateRange<Tz>) -> Result<()> {
        Ok(())
    }
}