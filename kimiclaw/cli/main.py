"""KimiClaw CLI - Command-line interface for managing the business OS."""

import click
import asyncio
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from kimiclaw.core.config import settings
from kimiclaw.core.ollama_client import OllamaClient
from kimiclaw.modules.lead_generation import LeadGenerationLoop

console = Console()


@click.group()
def cli():
    """🐝 KimiClaw Business OS - Your AI. Your data. Your business."""
    pass


@cli.command()
def status():
    """Show current system status and metrics."""
    console.print("\n[bold blue]🐝 KimiClaw Business OS[/bold blue]\n")
    
    # System info table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Business Name", settings.business_name)
    table.add_row("Industry", settings.business_industry.title())
    table.add_row("System Mode", settings.system_mode.upper())
    table.add_row("Language", settings.business_language.upper())
    table.add_row("Phone", settings.business_phone or "Not configured")
    
    console.print(table)
    
    # TODO: Add real-time metrics from database
    console.print("\n[bold yellow]📊 Today's Metrics[/bold yellow]\n")
    
    metrics_table = Table(show_header=False)
    metrics_table.add_column("Metric", style="cyan")
    metrics_table.add_column("Value", style="green", justify="right")
    
    metrics_table.add_row("Calendar Fill Rate", "65%")
    metrics_table.add_row("Calls Handled", "12")
    metrics_table.add_row("Leads Generated", "3")
    metrics_table.add_row("Revenue", "$1,250")
    
    console.print(metrics_table)
    console.print()


@cli.command()
@click.option('--count', default=10, help='Number of leads to search for')
def leads(count):
    """Run lead generation hunt."""
    console.print(f"\n[bold]🔍 Hunting for {count} leads...[/bold]\n")
    
    async def run_hunt():
        loop = LeadGenerationLoop()
        await loop.run_daily_hunt()
    
    asyncio.run(run_hunt())
    console.print("[green]✅ Lead hunt complete![/green]\n")


@cli.command()
def config():
    """Show current configuration."""
    console.print("\n[bold blue]⚙️  Configuration[/bold blue]\n")
    
    config_data = [
        ("Business Name", settings.business_name),
        ("Industry", settings.business_industry),
        ("Language", settings.business_language),
        ("Phone", settings.business_phone or "Not set"),
        ("WhatsApp", settings.business_whatsapp or "Not set"),
        ("", ""),
        ("Database URL", settings.database_url),
        ("Redis URL", settings.redis_url),
        ("Ollama Host", settings.ollama_host),
        ("", ""),
        ("System Mode", settings.system_mode),
        ("Auto Send Emails", str(settings.auto_send_emails)),
        ("Weekly Capacity", f"{settings.weekly_capacity} hours"),
    ]
    
    table = Table(show_header=False)
    table.add_column("Setting", style="cyan", width=30)
    table.add_column("Value", style="green")
    
    for key, value in config_data:
        if key == "":
            table.add_row("", "")
        else:
            table.add_row(key, value)
    
    console.print(table)
    console.print()


@cli.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=8000, help='Port to bind to')
def serve(host, port):
    """Start the FastAPI server."""
    console.print(f"\n[bold green]🚀 Starting KimiClaw Business OS on {host}:{port}[/bold green]\n")
    
    import uvicorn
    from kimiclaw.main import app
    
    uvicorn.run(app, host=host, port=port)


@cli.command()
@click.argument('prompt')
def ask(prompt):
    """Ask the AI a question."""
    console.print(f"\n[bold cyan]Question:[/bold cyan] {prompt}\n")
    
    async def get_answer():
        ollama = OllamaClient()
        
        system_prompt = f"""You are the AI assistant for {settings.business_name}, 
        a {settings.business_industry} business. Provide helpful, concise answers."""
        
        response = await ollama.generate(
            prompt=prompt,
            system=system_prompt,
            temperature=0.7
        )
        
        return response.get("response", "No response generated")
    
    answer = asyncio.run(get_answer())
    
    panel = Panel(answer, title="[bold green]Answer[/bold green]", border_style="green")
    console.print(panel)
    console.print()


@cli.command()
def models():
    """List available Ollama models."""
    console.print("\n[bold]🤖 Checking Ollama models...[/bold]\n")
    
    async def list_models():
        ollama = OllamaClient()
        try:
            models = await ollama.list_models()
            return models
        except Exception as e:
            console.print(f"[red]Error connecting to Ollama: {e}[/red]")
            console.print("\nMake sure Ollama is running: [cyan]ollama serve[/cyan]")
            return []
    
    models = asyncio.run(list_models())
    
    if models:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Model Name", style="cyan")
        table.add_column("Size", style="green")
        
        for model in models:
            name = model.get("name", "Unknown")
            size = model.get("size", 0)
            size_gb = size / (1024**3) if size else 0
            table.add_row(name, f"{size_gb:.1f} GB")
        
        console.print(table)
    
    console.print()


@cli.command()
def install():
    """Run the interactive installation wizard."""
    console.print("\n[bold blue]🐝 KimiClaw Business OS - Installation Wizard[/bold blue]\n")
    console.print("Answer these 8 questions to configure your AI business assistant:\n")
    
    # Question 1: Business Name
    business_name = console.input("[cyan]1. What is your business name?[/cyan] ")
    
    # Question 2: Industry
    console.print("\n[cyan]2. What industry are you in?[/cyan]")
    console.print("   Options: plumbing, electrical, hvac, landscaping, cleaning, general")
    industry = console.input("   Industry: ").lower()
    
    # Question 3: Phone Number
    phone = console.input("\n[cyan]3. What is your business phone number?[/cyan] ")
    
    # Question 4: WhatsApp Number
    whatsapp = console.input("[cyan]4. What is your WhatsApp number? (can be same as phone)[/cyan] ")
    
    # Question 5: Language
    console.print("\n[cyan]5. What language(s) do you serve customers in?[/cyan]")
    console.print("   Options: en (English), fr (French), bilingual (Both)")
    language = console.input("   Language: ").lower()
    
    # Question 6: Business Hours
    hours_start = console.input("\n[cyan]6. What time do you start work? (HH:MM format, e.g., 08:00)[/cyan] ")
    
    # Question 7: Business Hours End
    hours_end = console.input("[cyan]7. What time do you finish work? (HH:MM format, e.g., 17:00)[/cyan] ")
    
    # Question 8: Weekly Capacity
    capacity = console.input("\n[cyan]8. How many hours per week can you work? (e.g., 40)[/cyan] ")
    
    # Save configuration
    console.print("\n[bold green]✅ Configuration complete![/bold green]\n")
    console.print("Creating .env file...")
    
    env_content = f"""# KimiClaw Business OS Configuration
BUSINESS_NAME="{business_name}"
BUSINESS_INDUSTRY="{industry}"
BUSINESS_LANGUAGE="{language}"
BUSINESS_PHONE="{phone}"
BUSINESS_WHATSAPP="{whatsapp}"

BUSINESS_HOURS_START="{hours_start}"
BUSINESS_HOURS_END="{hours_end}"
WEEKLY_CAPACITY={capacity}

# System will auto-detect mode based on available RAM
SYSTEM_MODE="lite"
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    console.print("[green]✅ .env file created[/green]")
    console.print("\n[bold yellow]Next Steps:[/bold yellow]")
    console.print("1. Configure external services (Twilio, Google) in .env")
    console.print("2. Install Ollama: [cyan]curl https://ollama.ai/install.sh | sh[/cyan]")
    console.print("3. Pull AI models: [cyan]kimiclaw models[/cyan]")
    console.print("4. Start the server: [cyan]kimiclaw serve[/cyan]")
    console.print()


if __name__ == "__main__":
    cli()
