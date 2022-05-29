use crate::api::API;
use chrono::{DateTime, Local};

#[derive(Debug, clap::Args)]
pub struct Cat {
    #[clap(required = true)]
    company: String,
}

impl Cat {
    pub fn handler(&self, api: &impl API) {}
}
