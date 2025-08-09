import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from tkinter.ttk import Combobox
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandastable import Table  # Requires: pip install pandastable (version >= 0.13.1 recommended)

class StartupFundingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Startup Funding Analysis")
        self.root.geometry("1400x900")
        self.root.state('zoomed')  # Start maximized
        
        # Custom style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f8ff')
        self.style.configure('TLabel', background='#f0f8ff', font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10))
        self.style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'), foreground='#2e86de')
        
        # Initialize dataset
        self.df = None
        self.filtered_df = None
        
        # Create main container
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create title
        self.create_title()
        
        # Create notebook for tabs
        self.create_notebook()
        
        # Initialize UI components
        self.create_upload_panel()
        self.create_filter_panel()
        self.create_data_panel()
        self.create_visualization_panel()
        self.create_analysis_panel()
        
        # Initialize summary cards
        self.create_summary_cards()
        
    def create_title(self):
        title_frame = ttk.Frame(self.main_container)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(title_frame, text="Interactive Startup Funding Dashboard", style='Title.TLabel')
        title_label.pack()
        
        # Add a separator
        ttk.Separator(title_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
    
    def create_notebook(self):
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Create tabs
        self.data_tab = ttk.Frame(self.notebook)
        self.visualization_tab = ttk.Frame(self.notebook)
        self.analysis_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.data_tab, text="Data Management")
        self.notebook.add(self.visualization_tab, text="Visualization")
        self.notebook.add(self.analysis_tab, text="Analysis & Insights")
    
    def create_upload_panel(self):
        upload_frame = ttk.LabelFrame(self.data_tab, text="Data Upload & Cleaning", padding=(10, 5))
        upload_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Upload button
        upload_btn = ttk.Button(upload_frame, text="Upload Dataset", command=self.upload_dataset)
        upload_btn.pack(side=tk.LEFT, padx=5)
        
        # Cleaning buttons
        clean_steps_btn = ttk.Button(upload_frame, text="Show Cleaning Steps", command=self.show_cleaning_steps)
        clean_steps_btn.pack(side=tk.LEFT, padx=5)
        
        clean_data_btn = ttk.Button(upload_frame, text="Clean Data", command=self.clean_data)
        clean_data_btn.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(upload_frame, text="No dataset loaded")
        self.status_label.pack(side=tk.RIGHT, padx=5)
    
    def create_filter_panel(self):
        filter_frame = ttk.LabelFrame(self.data_tab, text="Interactive Filters", padding=(10, 5))
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Year filter
        ttk.Label(filter_frame, text="Year Range:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.year_min = ttk.Combobox(filter_frame, values=[], state='readonly', width=8)
        self.year_min.grid(row=0, column=1, padx=5)
        ttk.Label(filter_frame, text="to").grid(row=0, column=2)
        self.year_max = ttk.Combobox(filter_frame, values=[], state='readonly', width=8)
        self.year_max.grid(row=0, column=3, padx=5)
        
        # Sector filter
        ttk.Label(filter_frame, text="Industry Sector:").grid(row=0, column=4, sticky=tk.W, padx=5)
        self.sector_filter = ttk.Combobox(filter_frame, values=[], state='readonly', width=20)
        self.sector_filter.grid(row=0, column=5, padx=5)
        
        # City filter
        ttk.Label(filter_frame, text="City:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.city_filter = ttk.Combobox(filter_frame, values=[], state='readonly', width=20)
        self.city_filter.grid(row=1, column=1, columnspan=3, padx=5)
        
        # Investment type filter
        ttk.Label(filter_frame, text="Investment Type:").grid(row=1, column=4, sticky=tk.W, padx=5)
        self.investment_filter = ttk.Combobox(filter_frame, values=[], state='readonly', width=20)
        self.investment_filter.grid(row=1, column=5, padx=5)
        
        # Apply filter button
        filter_btn = ttk.Button(filter_frame, text="Apply Filters", command=self.apply_filters)
        filter_btn.grid(row=2, column=0, columnspan=6, pady=5)
        
        # Reset filter button
        reset_btn = ttk.Button(filter_frame, text="Reset Filters", command=self.reset_filters)
        reset_btn.grid(row=2, column=5, sticky=tk.E, padx=5, pady=5)
    
    def create_data_panel(self):
        data_display_frame = ttk.Frame(self.data_tab)
        data_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create a PandasTable for data display
        self.table_frame = ttk.Frame(data_display_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Placeholder for table
        self.table_label = ttk.Label(self.table_frame, text="Upload data to view interactive table")
        self.table_label.pack(expand=True)
    
    def create_visualization_panel(self):
        # Visualization controls frame
        controls_frame = ttk.Frame(self.visualization_tab)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Chart type selection
        ttk.Label(controls_frame, text="Chart Type:").pack(side=tk.LEFT, padx=5)
        self.chart_type = ttk.Combobox(controls_frame, 
                                      values=["Bar Plot", "Line Plot", "Pie Chart", "Scatter Plot", "Box Plot"], 
                                      state='readonly')
        self.chart_type.pack(side=tk.LEFT, padx=5)
        self.chart_type.set("Bar Plot")
        
        # X-axis selection
        ttk.Label(controls_frame, text="X-Axis:").pack(side=tk.LEFT, padx=5)
        self.x_axis = ttk.Combobox(controls_frame, state='readonly')
        self.x_axis.pack(side=tk.LEFT, padx=5)
        
        # Y-axis selection (for some chart types)
        ttk.Label(controls_frame, text="Y-Axis:").pack(side=tk.LEFT, padx=5)
        self.y_axis = ttk.Combobox(controls_frame, state='readonly')
        self.y_axis.pack(side=tk.LEFT, padx=5)
        
        # Group by selection
        ttk.Label(controls_frame, text="Group By:").pack(side=tk.LEFT, padx=5)
        self.group_by = ttk.Combobox(controls_frame, state='readonly')
        self.group_by.pack(side=tk.LEFT, padx=5)
        
        # Generate plot button
        plot_btn = ttk.Button(controls_frame, text="Generate Plot", command=self.generate_plot)
        plot_btn.pack(side=tk.LEFT, padx=10)
        
        # Export plot button
        export_btn = ttk.Button(controls_frame, text="Export Plot", command=self.export_plot)
        export_btn.pack(side=tk.RIGHT, padx=5)
        
        # Plot display frame
        self.plot_frame = ttk.Frame(self.visualization_tab)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Placeholder for plot
        self.plot_label = ttk.Label(self.plot_frame, text="Select chart options and click 'Generate Plot'")
        self.plot_label.pack(expand=True)
    
    def create_analysis_panel(self):
        # Analysis controls frame
        controls_frame = ttk.Frame(self.analysis_tab)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Analysis type selection
        ttk.Label(controls_frame, text="Analysis Type:").pack(side=tk.LEFT, padx=5)
        self.analysis_type = ttk.Combobox(controls_frame, 
                                        values=["Funding Trends", "Top Sectors", 
                                               "Top Startups", "Investor Activity", 
                                               "Geographical Distribution"],
                                        state='readonly')
        self.analysis_type.pack(side=tk.LEFT, padx=5)
        self.analysis_type.set("Funding Trends")
        
        # Run analysis button
        analyze_btn = ttk.Button(controls_frame, text="Run Analysis", command=self.run_analysis)
        analyze_btn.pack(side=tk.LEFT, padx=10)
        
        # Export analysis button
        export_btn = ttk.Button(controls_frame, text="Export Analysis", command=self.export_analysis)
        export_btn.pack(side=tk.RIGHT, padx=5)
        
        # Analysis display frame
        self.analysis_display = scrolledtext.ScrolledText(self.analysis_tab, wrap=tk.WORD, width=100, height=20)
        self.analysis_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.analysis_display.insert(tk.END, "Select an analysis type and click 'Run Analysis'")
        
        # Recommendations button
        recommend_btn = ttk.Button(self.analysis_tab, text="Show Recommendations", command=self.show_recommendations)
        recommend_btn.pack(pady=5)
    
    def create_summary_cards(self):
        summary_frame = ttk.Frame(self.main_container)
        summary_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Card 1: Total Funding
        self.card1 = ttk.Frame(summary_frame, style='Card.TFrame')
        ttk.Label(self.card1, text="Total Funding", style='CardTitle.TLabel').pack()
        self.total_funding_label = ttk.Label(self.card1, text="$0", style='CardValue.TLabel')
        self.total_funding_label.pack()
        self.card1.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        # Card 2: Number of Startups
        self.card2 = ttk.Frame(summary_frame, style='Card.TFrame')
        ttk.Label(self.card2, text="Startups", style='CardTitle.TLabel').pack()
        self.startups_label = ttk.Label(self.card2, text="0", style='CardValue.TLabel')
        self.startups_label.pack()
        self.card2.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        # Card 3: Top Sector
        self.card3 = ttk.Frame(summary_frame, style='Card.TFrame')
        ttk.Label(self.card3, text="Top Sector", style='CardTitle.TLabel').pack()
        self.top_sector_label = ttk.Label(self.card3, text="N/A", style='CardValue.TLabel')
        self.top_sector_label.pack()
        self.card3.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        # Card 4: Top City
        self.card4 = ttk.Frame(summary_frame, style='Card.TFrame')
        ttk.Label(self.card4, text="Top City", style='CardTitle.TLabel').pack()
        self.top_city_label = ttk.Label(self.card4, text="N/A", style='CardValue.TLabel')
        self.top_city_label.pack()
        self.card4.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        # Card 5: Avg Funding
        self.card5 = ttk.Frame(summary_frame, style='Card.TFrame')
        ttk.Label(self.card5, text="Avg Funding", style='CardTitle.TLabel').pack()
        self.avg_funding_label = ttk.Label(self.card5, text="$0", style='CardValue.TLabel')
        self.avg_funding_label.pack()
        self.card5.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        # Configure card styles
        self.style.configure('Card.TFrame', background='white', relief=tk.RAISED, borderwidth=1)
        self.style.configure('CardTitle.TLabel', background='white', font=('Helvetica', 9, 'bold'))
        self.style.configure('CardValue.TLabel', background='white', font=('Helvetica', 12))
    
    def upload_dataset(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            try:
                self.df = pd.read_csv(file_path, encoding='latin1')
                self.filtered_df = self.df.copy()
                self.status_label.config(text=f"Dataset loaded: {len(self.df)} records")
                
                # Initialize filters
                self.initialize_filters()
                
                # Show data in table
                self.display_data_table()
                
                # Update summary cards
                self.update_summary_cards()
                
                # Initialize visualization options
                self.initialize_visualization_options()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load dataset: {str(e)}")
    
    def initialize_filters(self):
        if self.df is None:
            return
            
        # Initialize year filter
        if 'date' in self.df.columns:
            self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
            self.df['year'] = self.df['date'].dt.year
            years = sorted(self.df['year'].dropna().unique())
            self.year_min['values'] = years
            self.year_max['values'] = years
            if years:
                self.year_min.set(years[0])
                self.year_max.set(years[-1])
        
        # Initialize sector filter
        if 'industry_vertical' in self.df.columns:
            sectors = ['All'] + sorted(self.df['industry_vertical'].dropna().unique().tolist())
            self.sector_filter['values'] = sectors
            self.sector_filter.set('All')
        
        # Initialize city filter
        if 'city_location' in self.df.columns:
            cities = ['All'] + sorted(self.df['city_location'].dropna().unique().tolist())
            self.city_filter['values'] = cities
            self.city_filter.set('All')
        
        # Initialize investment type filter
        if 'investment_type' in self.df.columns:
            inv_types = ['All'] + sorted(self.df['investment_type'].dropna().unique().tolist())
            self.investment_filter['values'] = inv_types
            self.investment_filter.set('All')
    
    def initialize_visualization_options(self):
        if self.df is None:
            return
            
        # Get all column names
        columns = self.df.columns.tolist()
        
        # Set options for x-axis and group by
        self.x_axis['values'] = columns
        self.group_by['values'] = ['None'] + columns
        
        # Set options for y-axis (numeric columns only)
        numeric_cols = self.df.select_dtypes(include=['number']).columns.tolist()
        self.y_axis['values'] = numeric_cols
        
        # Set default selections
        if 'amount_in_usd' in numeric_cols:
            self.y_axis.set('amount_in_usd')
        if 'industry_vertical' in columns:
            self.x_axis.set('industry_vertical')
        self.group_by.set('None')
    
    def display_data_table(self):
        if self.filtered_df is None:
            return
            
        # Clear previous table
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        # Create a PandasTable
        self.table = Table(self.table_frame, dataframe=self.filtered_df, showtoolbar=True, showstatusbar=True)
        self.table.show()
    
    def apply_filters(self):
        if self.df is None:
            return
            
        self.filtered_df = self.df.copy()
        
        # Apply year filter
        if 'year' in self.filtered_df.columns:
            try:
                min_year = int(self.year_min.get())
                max_year = int(self.year_max.get())
                self.filtered_df = self.filtered_df[(self.filtered_df['year'] >= min_year) & 
                                                  (self.filtered_df['year'] <= max_year)]
            except:
                pass
        
        # Apply sector filter
        sector = self.sector_filter.get()
        if sector != 'All' and 'industry_vertical' in self.filtered_df.columns:
            self.filtered_df = self.filtered_df[self.filtered_df['industry_vertical'] == sector]
        
        # Apply city filter
        city = self.city_filter.get()
        if city != 'All' and 'city_location' in self.filtered_df.columns:
            self.filtered_df = self.filtered_df[self.filtered_df['city_location'] == city]
        
        # Apply investment type filter
        inv_type = self.investment_filter.get()
        if inv_type != 'All' and 'investment_type' in self.filtered_df.columns:
            self.filtered_df = self.filtered_df[self.filtered_df['investment_type'] == inv_type]
        
        # Update table display
        self.display_data_table()
        
        # Update summary cards
        self.update_summary_cards()
        
        # Update status
        self.status_label.config(text=f"Showing {len(self.filtered_df)} of {len(self.df)} records")
    
    def reset_filters(self):
        if self.df is None:
            return
            
        self.filtered_df = self.df.copy()
        self.display_data_table()
        self.update_summary_cards()
        self.status_label.config(text=f"Showing all {len(self.df)} records")
        
        # Reset filter controls
        if 'year' in self.df.columns:
            years = sorted(self.df['year'].dropna().unique())
            if years:
                self.year_min.set(years[0])
                self.year_max.set(years[-1])
        
        self.sector_filter.set('All')
        self.city_filter.set('All')
        self.investment_filter.set('All')
    
    def update_summary_cards(self):
        if self.filtered_df is None:
            return
            
        # Total funding
        if 'amount_in_usd' in self.filtered_df.columns:
            total = self.filtered_df['amount_in_usd'].sum()
            self.total_funding_label.config(text=f"${total:,.2f}")
        
        # Number of startups
        if 'startup_name' in self.filtered_df.columns:
            count = self.filtered_df['startup_name'].nunique()
            self.startups_label.config(text=f"{count}")
        
        # Top sector
        if 'industry_vertical' in self.filtered_df.columns:
            top_sector = self.filtered_df['industry_vertical'].value_counts().idxmax()
            self.top_sector_label.config(text=top_sector)
        
        # Top city
        if 'city_location' in self.filtered_df.columns:
            top_city = self.filtered_df['city_location'].value_counts().idxmax()
            self.top_city_label.config(text=top_city)
        
        # Average funding
        if 'amount_in_usd' in self.filtered_df.columns:
            avg = self.filtered_df['amount_in_usd'].mean()
            self.avg_funding_label.config(text=f"${avg:,.2f}")
    
    def show_cleaning_steps(self):
        if self.df is None:
            messagebox.showerror("Error", "Please upload dataset first")
            return
            
        # Create a new window for cleaning steps
        clean_window = tk.Toplevel(self.root)
        clean_window.title("Data Cleaning Report")
        clean_window.geometry("800x600")
        
        # Create text widget
        text = scrolledtext.ScrolledText(clean_window, wrap=tk.WORD, width=100, height=30)
        text.pack(fill=tk.BOTH, expand=True)
        
        # Generate cleaning report
        text.insert(tk.END, "Dataset Cleaning Report (Before Cleaning):\n\n")
        
        # Column names before cleaning
        text.insert(tk.END, "Original Column Names:\n")
        text.insert(tk.END, f"{list(self.df.columns)}\n\n")
        
        # Detect columns with spaces in names
        spaces_in_columns = [col for col in self.df.columns if ' ' in col or col != col.strip()]
        if spaces_in_columns:
            text.insert(tk.END, f"Columns with spaces: {spaces_in_columns}\n\n")
        
        # Null value report
        text.insert(tk.END, "Null Values per Column:\n")
        text.insert(tk.END, f"{self.df.isnull().sum()}\n\n")
        
        # Data types
        text.insert(tk.END, "Current Data Types:\n")
        text.insert(tk.END, f"{self.df.dtypes}\n\n")
        
        # Check Amount in USD issues
        if 'Amount in USD' in self.df.columns:
            invalid_amount = self.df['Amount in USD'].astype(str).str.contains('[^0-9,]', na=False).sum()
            text.insert(tk.END, f"'Amount in USD' entries with non-numeric values: {invalid_amount}\n\n")
        
        # Check Date issues
        if 'Date' in self.df.columns:
            invalid_dates = pd.to_datetime(self.df['Date'], errors='coerce').isnull().sum()
            text.insert(tk.END, f"Invalid date entries: {invalid_dates}\n\n")
        
        text.insert(tk.END, "These are the issues that will be fixed in cleaning.\n")
    
    def clean_data(self):
        if self.df is None:
            messagebox.showerror("Error", "Please upload dataset first")
            return
            
        try:
            # 1. Standardize column names
            self.df.columns = self.df.columns.str.strip().str.lower().str.replace(' ', '_')
            
            # 2. Drop completely empty rows
            self.df.dropna(how='all', inplace=True)
            
            # 3. Handle City column
            if 'city_location' in self.df.columns:
                # Fill NaN with 'Unknown'
                self.df['city_location'] = self.df['city_location'].fillna("Unknown")
                
                # Clean formatting
                self.df['city_location'] = (
                    self.df['city_location']
                    .astype(str)
                    .str.strip()
                    .str.title()
                )
                
                # Standardize common variations
                city_map = {
                    'Bangalore': 'Bengaluru',
                    'Delhi': 'Delhi NCR',
                    'New Delhi': 'Delhi NCR',
                    'Ncr': 'Delhi NCR',
                    'Gurgaon': 'Delhi NCR',
                    'Noida': 'Delhi NCR',
                    'Bombay': 'Mumbai'
                }
                self.df['city_location'] = self.df['city_location'].replace(city_map)
            else:
                self.df['city_location'] = "Unknown"
            
            # 4. Handle Date column
            if 'date' in self.df.columns:
                self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
                self.df['year'] = self.df['date'].dt.year
            
            # 5. Clean Amount column
            if 'amount_in_usd' in self.df.columns:
                self.df['amount_in_usd'] = (
                    self.df['amount_in_usd']
                    .astype(str)
                    .str.replace(',', '', regex=False)
                    .str.strip()
                )
                self.df['amount_in_usd'] = pd.to_numeric(
                    self.df['amount_in_usd'].replace("undisclosed", None),
                    errors='coerce'
                )
                # Fill missing amounts with 0 instead of dropping
                self.df['amount_in_usd'] = self.df['amount_in_usd'].fillna(0)
            else:
                self.df['amount_in_usd'] = 0
            
            # 6. Fill other important text columns with "Unknown"
            for col in ['startup_name', 'industry_vertical']:
                if col in self.df.columns:
                    self.df[col] = self.df[col].fillna("Unknown")
            
            # 7. Reset index
            self.df.reset_index(drop=True, inplace=True)
            
            # Update filtered df
            self.filtered_df = self.df.copy()
            
            # Update UI
            self.display_data_table()
            self.initialize_filters()
            self.initialize_visualization_options()
            self.update_summary_cards()
            
            messagebox.showinfo("Success", "Data cleaned successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Data cleaning failed: {str(e)}")
    
    def generate_plot(self):
        if self.filtered_df is None or self.filtered_df.empty:
            messagebox.showerror("Error", "No data to visualize. Please upload and filter data first.")
            return
            
        chart_type = self.chart_type.get()
        x_var = self.x_axis.get()
        y_var = self.y_axis.get() if self.y_axis.get() else None
        group_var = self.group_by.get() if self.group_by.get() != 'None' else None
        
        # Clear previous plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        try:
            plt.figure(figsize=(10, 6))
            
            if chart_type == "Bar Plot":
                if group_var:
                    sns.barplot(data=self.filtered_df, x=x_var, y=y_var, hue=group_var)
                else:
                    if y_var:
                        sns.barplot(data=self.filtered_df, x=x_var, y=y_var)
                    else:
                        # Count plot if no y_var specified
                        sns.countplot(data=self.filtered_df, y=x_var, order=self.filtered_df[x_var].value_counts().index)
            
            elif chart_type == "Line Plot":
                if y_var:
                    if group_var:
                        sns.lineplot(data=self.filtered_df, x=x_var, y=y_var, hue=group_var)
                    else:
                        sns.lineplot(data=self.filtered_df, x=x_var, y=y_var)
                else:
                    messagebox.showerror("Error", "Line plot requires a Y-axis variable")
                    return
            
            elif chart_type == "Pie Chart":
                if not y_var:
                    # Count values for pie chart
                    counts = self.filtered_df[x_var].value_counts().head(10)
                    plt.pie(counts, labels=counts.index, autopct='%1.1f%%')
                else:
                    messagebox.showerror("Error", "Pie chart only supports single variable")
                    return
            
            elif chart_type == "Scatter Plot":
                if y_var:
                    if group_var:
                        sns.scatterplot(data=self.filtered_df, x=x_var, y=y_var, hue=group_var)
                    else:
                        sns.scatterplot(data=self.filtered_df, x=x_var, y=y_var)
                else:
                    messagebox.showerror("Error", "Scatter plot requires X and Y variables")
                    return
            
            elif chart_type == "Box Plot":
                if y_var:
                    if group_var:
                        sns.boxplot(data=self.filtered_df, x=x_var, y=y_var, hue=group_var)
                    else:
                        sns.boxplot(data=self.filtered_df, x=x_var, y=y_var)
                else:
                    sns.boxplot(data=self.filtered_df, y=x_var)
            
            plt.title(f"{chart_type} of {x_var}" + (f" vs {y_var}" if y_var else ""))
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Embed plot in Tkinter
            canvas = FigureCanvasTkAgg(plt.gcf(), master=self.plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate plot: {str(e)}")
    
    def export_plot(self):
        # This would save the current plot to a file
        messagebox.showinfo("Info", "This would export the current plot in a real implementation")
    
    def run_analysis(self):
        if self.filtered_df is None or self.filtered_df.empty:
            messagebox.showerror("Error", "No data to analyze. Please upload and filter data first.")
            return
            
        analysis_type = self.analysis_type.get()
        self.analysis_display.delete('1.0', tk.END)
        
        try:
            if analysis_type == "Funding Trends":
                if 'date' in self.filtered_df.columns and 'amount_in_usd' in self.filtered_df.columns:
                    funding_trend = self.filtered_df.groupby(self.filtered_df['date'].dt.year)['amount_in_usd'].sum()
                    self.analysis_display.insert(tk.END, "Funding Trends by Year:\n")
                    self.analysis_display.insert(tk.END, funding_trend.to_string())
                else:
                    self.analysis_display.insert(tk.END, "Required columns (date, amount_in_usd) not available")
            
            elif analysis_type == "Top Sectors":
                if 'industry_vertical' in self.filtered_df.columns:
                    top_sectors = self.filtered_df['industry_vertical'].value_counts().head(10)
                    self.analysis_display.insert(tk.END, "Top 10 Sectors by Startup Count:\n")
                    self.analysis_display.insert(tk.END, top_sectors.to_string())
                else:
                    self.analysis_display.insert(tk.END, "industry_vertical column not available")
            
            elif analysis_type == "Top Startups":
                if 'startup_name' in self.filtered_df.columns and 'amount_in_usd' in self.filtered_df.columns:
                    top_startups = self.filtered_df.groupby('startup_name')['amount_in_usd'].sum().nlargest(10)
                    self.analysis_display.insert(tk.END, "Top 10 Startups by Total Funding:\n")
                    self.analysis_display.insert(tk.END, top_startups.to_string())
                else:
                    self.analysis_display.insert(tk.END, "Required columns (startup_name, amount_in_usd) not available")
            
            elif analysis_type == "Investor Activity":
                if 'investors_name' in self.filtered_df.columns:
                    top_investors = self.filtered_df['investors_name'].value_counts().head(10)
                    self.analysis_display.insert(tk.END, "Top 10 Most Active Investors:\n")
                    self.analysis_display.insert(tk.END, top_investors.to_string())
                else:
                    self.analysis_display.insert(tk.END, "investors_name column not available")
            
            elif analysis_type == "Geographical Distribution":
                if 'city_location' in self.filtered_df.columns and 'amount_in_usd' in self.filtered_df.columns:
                    geo_dist = self.filtered_df.groupby('city_location')['amount_in_usd'].sum().nlargest(10)
                    self.analysis_display.insert(tk.END, "Top 10 Cities by Total Funding:\n")
                    self.analysis_display.insert(tk.END, geo_dist.to_string())
                else:
                    self.analysis_display.insert(tk.END, "Required columns (city_location, amount_in_usd) not available")
            
        except Exception as e:
            self.analysis_display.insert(tk.END, f"Analysis failed: {str(e)}")
    
    def export_analysis(self):
        # This would save the current analysis to a file
        messagebox.showinfo("Info", "This would export the current analysis in a real implementation")
    
    def show_recommendations(self):
        if self.filtered_df is None:
            messagebox.showerror("Error", "Please upload and clean dataset first")
            return
            
        # Get top sectors
        top_sector = "N/A"
        if 'industry_vertical' in self.filtered_df.columns:
            top_sector = self.filtered_df['industry_vertical'].value_counts().idxmax()
        
        # Get top cities
        top_cities = ["N/A"]
        if 'city_location' in self.filtered_df.columns:
            top_cities = self.filtered_df['city_location'].value_counts().head(3).index.tolist()
        
        # Get top investors
        top_investors = ["N/A"]
        if 'investors_name' in self.filtered_df.columns:
            top_investors = self.filtered_df['investors_name'].value_counts().head(3).index.tolist()
        
        # Get funding trends
        funding_trend = "N/A"
        if 'date' in self.filtered_df.columns and 'amount_in_usd' in self.filtered_df.columns:
            trend = self.filtered_df.groupby(self.filtered_df['date'].dt.year)['amount_in_usd'].sum()
            funding_trend = "Increasing" if len(trend) > 1 and trend.iloc[-1] > trend.iloc[0] else "Decreasing"
        
        # Generate recommendations
        recommendations = f"""
Recommendations Based on Current Data:

1. Focus on top funding sector: {top_sector}
2. Target top startup hubs: {", ".join(top_cities)}
3. Engage with active investors: {", ".join(top_investors)}
4. Funding trend is currently {funding_trend} - adjust strategy accordingly
5. Consider seasonal patterns in funding dates for optimal fundraising
6. Analyze competitor funding rounds for benchmarking
7. Explore emerging sectors with fewer but larger investments
        """
        
        self.analysis_display.delete('1.0', tk.END)
        self.analysis_display.insert(tk.END, recommendations)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = StartupFundingApp(root)
    root.mainloop()