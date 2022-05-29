use crate::api::{API, FreeDateArgs};
use crate::util::{format_date, format_time};

#[derive(Debug, clap::Args)]
pub struct Ls {}

impl Ls {
    pub fn handler(&self, api: &impl API) {
        match api.check_free_date(&FreeDateArgs {}){
            Ok(dates) => {
                println!("現在空いている日程は以下のとおりです。");
                let content = dates.join("\n");
                println!("{}", content)
            },
            Err(why) => {
                println!("エラーが発生しました\n{}", why)
            }
        };
    }
}
