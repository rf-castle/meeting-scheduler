use chrono::{DateTime, Local};
use crate::api::API;

#[derive(Debug, clap::Args)]
pub struct Cat {
    #[clap(required=true)]
    company: String
}

impl Cat {
    pub fn handler(&self, api: &impl API){

    }
}
