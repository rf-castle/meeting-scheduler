use chrono::Utc;

#[derive(Debug, clap::Args)]
struct Commit {
    #[clap(required=true)]
    company: String,
    #[clap(required=true)]
    start: chrono::DateTime<Utc>,
    #[clap(required_unless_present="duration",conflicts_with="duration")]
    end: Option<chrono::DateTime<Utc>>,
    duration: Option<u64>,
}

fn handler(args: &Commit){

}