use chrono::{Local};
use crate::api::API;
use crate::util::{format_date, format_datetime, format_time, parse_date};

#[derive(Debug, clap::Args)]
pub struct Commit {
    #[clap(required=true)]
    company: String,
    #[clap(required=true, parse(try_from_str = parse_date))]
    start: chrono::DateTime<Local>,
    // Todo: 長さだけあれするのはなぁ
    duration: Option<i64>,
    #[clap(
        required_unless_present="duration",
        conflicts_with="duration",
        parse(try_from_str = parse_date),
    )]
    // Todo: 上の引数のパースが失敗したときにこっちも試す
    end: Option<chrono::DateTime<Local>>,
}


impl Commit{
    pub fn handler(&self, api: &impl API){
        let Commit {
            company,
            start,
            ..
        } = self;
        let end = match self.end {
            Some(x) => {x},
            None => {self.start + chrono::Duration::minutes(self.duration.unwrap())}
        };
        match api.decide_date(company, &(*start, end)){
            Ok(_) => {
                println!(
                    "{}の面接日程を{} {}~{}に決定しました。",
                    company,
                    format_date(&start.naive_local().date()),
                    format_time(&start.time()),
                    format_time(&end.time()),
                )
            },
            Err(why) => {
                println!("エラーが発生しました\n{}", why)
            },
        };
    }
}
