use crate::api::API;
use crate::util::{format_date, format_time, parse_date};
use chrono::{DateTime, Local};

#[derive(Debug, clap::Args)]
pub struct Reserve {
    #[clap(required = true)]
    company: String,
    #[clap(
    parse(try_from_str = parse_date),
    )]
    dates: Vec<DateTime<Local>>,
}

impl Reserve {
    pub fn handler(&self, api: &impl API) {
        let mut date_args = self.dates.clone().into_iter().rev().collect::<Vec<_>>();
        let mut dates = Vec::new();
        'outer: while let Some(start) = date_args.pop() {
            while let Some(end) = date_args.pop() {
                dates.push((start, end));
                continue 'outer;
            }
        }
        match api.reserve_date(&self.company, &dates) {
            Ok(_) => {
                println!("以下の日程を{}の面接候補として設定しました。", self.company);
                let content = dates
                    .iter()
                    .map(|(d1, d2)| {
                        format!(
                            "{} {} {}",
                            format_date(d1.naive_local().date()),
                            format_time(d1.time()),
                            format_time(d2.time())
                        )
                    })
                    .collect::<Vec<String>>()
                    .join("\n");
                println!("{}", content)
            }
            Err(why) => {
                println!("エラーが発生しました\n{}", why)
            }
        };
    }
}
