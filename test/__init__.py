import hypothesis

# #################################################################################### #
#                                Hypothesis Setup
# #################################################################################### #

hypothesis.settings.register_profile(
    "dev",
    print_blob=True,
    suppress_health_check=(hypothesis.HealthCheck.too_slow,),
)
hypothesis.settings.load_profile("dev")
print(f"hypothesis.settings.print_blob == {hypothesis.settings.print_blob}")
