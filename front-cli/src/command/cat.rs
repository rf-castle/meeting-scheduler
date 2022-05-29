use crate::api::API;
use reqwest::Result;

#[derive(Debug, clap::Args)]
pub struct Cat {
    company: Option<String>,
}

impl Cat {
    fn _handler(&self, api: &impl API) -> Result<()>{
        match &self.company {
            Some(company) => {
                let dates = api.search_reserved_date(company)?;
                println!("現在{}の日程候補として設定されているのは以下の日程です。", company);
                let content = dates.join("\n");
                println!("{}", content)
            },
            None => {
                let dates = api.search_reserved_dates()?;
                println!("現在日程候補として設定されているのは以下の日程です。");
                dates.iter().for_each(|(k, v)|{
                    println!("{}", k);
                    println!("{}\n\n", v.join(", "));
                });
            }
        }
        Ok(())
    }
    pub fn handler(&self, api: &impl API) {
        if let Err(why) = self._handler(api){
            println!("エラーが発生しました\n{}", why);
        }
    }
}
