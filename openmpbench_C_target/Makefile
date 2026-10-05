include Makefile.defs.nvc

SRC     := src/microbenchmark.c src/common.c
OBJ     := $(SRC:.c=.o)

BIN     := microbenchmark
BIN_DISTRIBUTION := microbenchmark_distribution

# -------------------------- Build Targets -------------------------------

all: $(BIN)

# Default build (no overhead logging)
$(BIN): $(SRC)
	$(CC) $(CFLAGS) -o $@ $(SRC) $(LDFLAGS) $(LIBS)

# Distribution build with PRINT_DISTRIBUTION enabled
distribution: $(SRC)
	$(CC) $(CFLAGS) -DPRINT_DISTRIBUTION -o $(BIN_DISTRIBUTION) $(SRC) $(LDFLAGS) $(LIBS)

# Run all benchmark methods and log output
run_all: $(BIN)
	mkdir -p Output
	./$(BIN) Method=1,2,3,4,5,6,7,8,9,10,11 N=16384 thread_count=32 team_count=4 > Output/full_run_$(shell date +%Y%m%d_%H%M%S).out 2>&1

# Run overhead logging plot benchmarks
run_plot: $(BIN_DISTRIBUTION)
	./$(BIN_DISTRIBUTION) Method=5,6,10,11 N=16384 thread_count=32 team_count=4

# Help message
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  all             - Build main microbenchmark (default)"
	@echo "  distribution    - Build with overhead distribution logging enabled"
	@echo "  run_all         - Run all methods and save output to timestamped file"
	@echo "  run_plot        - Run selected methods with distribution output"
	@echo "  clean           - Remove binaries and logs"
	@echo "  help            - Show this help message"

# Clean all
clean:
	rm -f $(BIN) $(BIN_DISTRIBUTION) *.o *.out overhead_distribution.txt

.PHONY: all distribution run_all run_plot clean help
