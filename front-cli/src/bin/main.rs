use clap::Parser;
use front_cli::command::*;
use front_cli::APIImpl;

#[derive(Debug, Parser)]
pub enum Commands {
    /// 面接日程を確定させます
    #[clap(name = "commit")]
    Commit(Commit),
    Ls(Ls),
    Reserve(Reserve),
    Cat(Cat),
}

fn main() {
    let api = APIImpl::new();
    let args = Commands::parse();
    match args {
        Commands::Commit(args) => args.handler(&api),
        Commands::Ls(args) => args.handler(&api),
        Commands::Reserve(args) => args.handler(&api),
        Commands::Cat(args) => args.handler(&api),
    };
}
