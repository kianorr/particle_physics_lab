import ROOT
class HistogramViaRoot():
    def __init__(self, TDC_number, root_file, t_min=0, t_max=1000, bins=50, out_file=None, up_hist=None, down_hist=None):
        self.t_min = t_min
        self.t_max = t_max
        self.bins = bins
        self.file_in = ROOT.TFile.Open(root_file, "READ")
        self.tree = self.file_in.Get("data")
        
        self.TDC_number = TDC_number
        if TDC_number == "TDC6":
            hist_title = "Up (TDC6) Histogram"
        elif TDC_number == "TDC7":
            hist_title = "Down (TDC7) Histogram"
        else:
            hist_title = "Asymmetry"
        self.histo = ROOT.TH1D("histo", f"{hist_title}", bins, t_min, t_max)
        self.sum_hist = ROOT.TH1D("sum_hist", f"{hist_title}", bins, t_min, t_max)
        self.difference_hist = ROOT.TH1D("difference_hist", f"{hist_title}", bins, t_min, t_max)
        
        if out_file != None:
            self.out_file = out_file
        if up_hist != None:
            self.up_hist = up_hist
        if down_hist != None:
            self.down_hist = down_hist
        
    def get_axis_labels(self, y_label):
        self.histo.GetXaxis().SetTitle("Time on TDC (ns)")
        self.histo.GetXaxis().CenterTitle(True)
        self.histo.GetYaxis().SetTitle(f"{y_label}")
        self.histo.GetYaxis().CenterTitle(True)
        
    def draw_up_histogram(self):
    	self.up_hist = ROOT.TH1D("up_hist","TDC6 Histogram (Up events)", self.bins, self.t_min, self.t_max)
    	self.tree.Draw("TDC6*20>>up_hist", "TDC6>0")
    	
    def draw_down_histogram(self):
    	self.down_hist = ROOT.TH1D("down_hist","TDC7 Histogram (Down events)", self.bins, self.t_min, self.t_max)
    	self.tree.Draw("TDC7*20>>down_hist", "TDC7>0")
    
    def draw_combined_histogram(self, hist_type):
    	difference = self.up_hist + (-1 * self.down_hist)
    	summ = self.up_hist + self.down_hist
#    	self.difference_hist.Add(self.up_hist, -1*self.down_hist)
#    	print(self.difference_hist.GetEntries())
#    	self.sum_hist.Add(self.up_hist, self.down_hist)
#    	print(self.sum_hist.GetEntries())
    	if hist_type == "difference":
    	    self.histo.Add(self.up_hist, -1 * self.down_hist)
    	elif hist_type == "sum":
    	    self.histo.Add(self.up_hist, self.down_hist)
    	elif hist_type == "asymmetry":
#    	    self.histo = ROOT.TGraphAsymmErrors(difference, summ)
#    	    self.histo.BayesDivide(difference, summ, opt="b")
#    	    self.histo.Draw("ACP")
    	    self.histo.Divide(difference, summ)
    	
    	self.histo.Draw()
    	print("\nsum")
    	for i in range(13):
    	    print(self.histo.GetBinContent(i))
    	print("\nup")
    	for i in range(13):
    	    print(self.up_hist.GetBinContent(i))
    	print("\ndown")
    	for i in range(13):
    	    print(self.down_hist.GetBinContent(i))
    	print(self.histo.GetEntries())
        
    def draw_asymmetry_histogram(self):
        U = ROOT.TH1D("U","TDC6 Histogram (Up events)", self.bins, self.t_min, self.t_max)
        D = ROOT.TH1D("D","TDC 7 Histogram (Down events)", self.bins, self.t_min, self.t_max)
        self.tree.Draw("TDC6*20>>U", "TDC6>0")
        self.tree.Draw("TDC7*20>>D", "TDC7>0")
        difference = U + (-1 * D)
        summ = U + D
        self.histo.Divide(difference, summ)
        self.histo.Draw()
        
    def get_expo_fit(self):
        self.histo.Sumw2()
        func = ROOT.TF1("func", "[0]*exp(-x/[1])", 0, 5000)
        func.SetParameters(0, 1)
        func.SetParameters(1, 1000)
        func.Draw()
        if self.TDC_number == "TDC6":
            self.up_hist.Fit(func, "", "", 400, 5000)
        elif self.TDC_number == "TDC7":
            self.down_hist.Fit(func, "", "", 400, 5000)
        
    def get_ticho_fit(self):
    	func = ROOT.TF1("func", "(exp(-[0]*x)*([1]+[2]*cos([3]*x)))", self.t_min, self.t_max)
    	func.SetParameters(1, 1, 1, 1)
    	func.Draw()
    	self.histo.Fit(func, "", "", self.t_min, self.t_max)
        
    def get_asymm_fit(self):
#         self.histo.Sumw2()
        func = ROOT.TF1("func", "([1]+[2]*cos([3]*x + [4]))", self.t_min, self.t_max)
        func.SetParameters(1, 1, 1, 1)
        func.Draw()
        self.histo.Fit(func, "", "", self.t_min, self.t_max)
        
    def set_out_file(self, out_file_name):
        self.out_file = ROOT.TFile.Open(out_file_name, "RECREATE")
        self.out_file.cd()
        
    def write_histogram(self):
        self.histo.SetDirectory(self.out_file)
        self.histo.Write()
    
    def close_files(self):
        self.file_in.Close()
        self.out_file.Close()
        
if __name__ == "__main__":
    root_file = "all_root_files.root"
    h = HistogramViaRoot(None, root_file, t_min=0, t_max=700, bins=14)
    #h.draw_lifetime_histogram()
    #h.get_expo_fit()
    #h.draw_asymmetry_histogram()
    h.draw_down_histogram()
    h.draw_up_histogram()
    h.draw_combined_histogram("asymmetry")
    #h.get_ticho_fit()
    #h.get_asymm_fit()
    h.set_out_file("asymmetry_hist.root")
    h.write_histogram()
    h.close_files()
