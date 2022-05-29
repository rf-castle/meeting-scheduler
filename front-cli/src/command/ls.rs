use crate::api::{API, FreeDateArgs};
use crate::util::{format_date, format_time};

#[derive(Debug, clap::Args)]
pub struct Ls {}

impl Ls {
    pub fn handler(&self, api: &impl API) {
        match api.check_free_date(&FreeDateArgs {}){
            Ok(dates) => {
                println!("現在空いている日程は以下のとおりです。");
                // Todo: 関数化しろ
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
            },
            Err(why) => {
                println!("エラーが発生しました\n{}", why)
            }
        };
    }
}
