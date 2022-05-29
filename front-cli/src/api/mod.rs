use std::collections::HashMap;
use chrono::{DateTime, TimeZone, Utc};
use const_format::concatcp;
use maplit::hashmap;
use reqwest::blocking::Client;
use reqwest::Result;
use std::fmt;
use serde::Deserialize;

const ENDPOINT: &str = "http://localhost:9000";

type DateRange<Tz> = (DateTime<Tz>, DateTime<Tz>);

#[derive(Default, Clone)]
pub struct FreeDateArgs {}

pub trait API {
    // Todo: ログイン
    fn search_reserved_date(&self, company: &str) -> Result<()>;
    fn check_free_date(&self, args: &FreeDateArgs) -> Result<Vec<DateRange<Utc>>>;
    fn reserve_date<Tz: TimeZone>(&self, company: &str, dates: &[DateRange<Tz>]) -> Result<()>
    where
        Tz::Offset: fmt::Display;
    fn decide_date<Tz: TimeZone>(&self, company: &str, date: &DateRange<Tz>) -> Result<()>
    where
        Tz::Offset: fmt::Display;
}

pub struct APIImpl {
    client: Client,
}

impl APIImpl {
    pub fn new() -> Self {
        APIImpl {
            client: Client::new(),
        }
    }
}

fn date_for_api<Tz: TimeZone>(range: &DateRange<Tz>) -> String
where
    Tz::Offset: fmt::Display,
{
    format!(
        "{} - {}",
        range.0.format("%m/%d %H:%M"),
        range.1.format("%H:%M")
    )
}


impl API for APIImpl {
    fn search_reserved_date(&self, company: &str) -> Result<()> {
        Ok(())
    }

    fn check_free_date(&self, args: &FreeDateArgs) -> Result<Vec<DateRange<Utc>>> {
        let response = self.client
            .get(concatcp!(ENDPOINT, "/empty-dates"))
            .send()?
            .error_for_status()?;
        let body: HashMap<String, Vec<String>> = response.json()?;
        Ok(vec![])
    }

    fn reserve_date<Tz: TimeZone>(&self, company: &str, dates: &[DateRange<Tz>]) -> Result<()>
    where
        Tz::Offset: fmt::Display,
    {
        let map = hashmap! {
            "company" => company.to_string(),
            "candidate_dates" => format!(
                "[{}]",
                dates.iter()
                    .map(|s|format!("\"{}\"", date_for_api(s)))
                    .collect::<Vec<String>>()
                    .join(",")
            ),
        };
        self.client
            .post(concatcp!(ENDPOINT, "/candidate-dates"))
            .form(&map)
            .send()?
            .error_for_status()?;
        Ok(())
    }

    fn decide_date<Tz: TimeZone>(&self, company: &str, date: &DateRange<Tz>) -> Result<()>
    where
        Tz::Offset: fmt::Display,
    {
        let map = hashmap! {
            "company" => company.to_string(),
            "candidate_dates" => date_for_api(date),
        };
        self.client
            .post(concatcp!(ENDPOINT, "/interview-date"))
            .form(&map)
            .send()?
            .error_for_status()?;
        Ok(())
    }
}
