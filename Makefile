all: sim exp

sim: sim/README.md sim/particle_configuration.dat sim/colour_output_t00250000-0285621391.h5

exp: exp/README.txt exp/CoarseSand_Day2Growth.tif exp/CoarseSand_Day6Growth.tif exp/FineSand_Day2Growth.tif exp/FineSand_Day6Growth.tif

# Simulated data (phase field dataset)
sim/README.md:
	wget -O $@ "https://data.4tu.nl/file/9f2f96b0-99a6-439b-848e-e914f51d7d85/a19626bc-0b37-41a1-8671-ea28b4b4017f"

sim/particle_configuration.dat:
	wget -O $@ "https://data.4tu.nl/file/9f2f96b0-99a6-439b-848e-e914f51d7d85/cdf3fcab-00ea-44ff-aeb7-fe043ed4a9ba"

sim/colour_output_t00250000-0285621391.h5:
	wget -O $@ "https://data.4tu.nl/file/9f2f96b0-99a6-439b-848e-e914f51d7d85/83b4abe7-54f1-4f36-8e2b-6e2e604adca0"

# Experimental data (X-Ray dataset)
exp/README.txt:
	wget -O $@ "https://data.4tu.nl/file/f249ac1c-9eed-49a8-8341-8be4bf4296b0/f0f8b41c-cee3-4fe1-a34d-f0e803060079"

exp/CoarseSand_Day2Growth.tif:
	wget -O $@ "https://data.4tu.nl/file/f249ac1c-9eed-49a8-8341-8be4bf4296b0/d2cffe40-61af-434b-8e57-874a7e1e3f52"

exp/CoarseSand_Day6Growth.tif:
	wget -O $@ "https://data.4tu.nl/file/f249ac1c-9eed-49a8-8341-8be4bf4296b0/ec91538f-b005-4fae-adb5-3e2372169ff3"

exp/FineSand_Day2Growth.tif:
	wget -O $@ "https://data.4tu.nl/file/f249ac1c-9eed-49a8-8341-8be4bf4296b0/aa7741b3-85ec-47d3-89e0-79e08828ea60"

exp/FineSand_Day6Growth.tif:
	wget -O $@ "https://data.4tu.nl/file/f249ac1c-9eed-49a8-8341-8be4bf4296b0/fb171e68-03a1-4a60-b179-60634085f3d0"