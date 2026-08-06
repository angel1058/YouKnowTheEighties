namespace MauiTestFlightApp;

public partial class MainPage : ContentPage
{
	private int _count = 0;

	public MainPage()
	{
		InitializeComponent();
	}

	private void OnCounterClicked(object sender, EventArgs e)
	{
		_count++;

		CounterDisplay.Text = $"{_count}";

		if (_count == 1)
		{
			CounterBtn.Text = "Clicked 1 time 🎉";
			CounterStatus.Text = "Great start! App state is working properly.";
		}
		else
		{
			CounterBtn.Text = $"Clicked {_count} times 🎉";
			CounterStatus.Text = $"Counter updated successfully ({_count} total clicks).";
		}

		SemanticScreenReader.Announce(CounterBtn.Text);
	}
}
