use chrono::{DateTime, Local};
use crate::api::API;
use crate::util::parse_date;

#[derive(Debug, clap::Args)]
pub struct Reserve {
    #[clap(required=true)]
    company: String,
    #[clap(
    required_unless_present="duration",
    conflicts_with="duration",
    parse(try_from_str = parse_date),
    )]
    dates: Vec<DateTime<Local>>
}

impl Reserve{
    pub fn handler(&self, api: &impl API){
        let mut date_args = self.dates.clone();
        let mut dates = Vec::new();
        while let Some(start) = date_args.pop() {
            while let Some(end) = date_args.pop() {
                dates.push((start, end));
            }
        }
        match api.reserve_date(&self.company, &dates){
            Ok(_) => {
                println!("以下の日程を{}の面接候補として設定しました。", self.company);
            },
            Err(why) => {
                println!("エラーが発生しました\n{}", why)
            },
        };
    }
}
