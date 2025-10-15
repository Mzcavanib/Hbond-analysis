These programs are designed to streamline the analysis of hydrogen bonds in GROMACS, specifically those extracted using the command:

```
gmx or gmx_mpi hbond -f md.xtc -s md.tpr -n index.ndx -hbn hbond.ndx -hbm hbond.xpm -num hbond.xvg
```

Based on the output from this command, I developed the script `hbond_traj.py`, which analyzes the `hbond.xvg` file to quantify the abundance of hydrogen bonds per frame throughout the simulation. Together with `hbond_vs_time.py`, these tools provide a comprehensive analysis of the `hbond.xvg` dataset.

To use these scripts, simply place them in the same directory as the relevant files—they automatically detect and read the required inputs.

Finally, I present `hbondkernel.py`, a script that plots hydrogen bond count versus density using kernel density estimation. This visualization is intended for comparing multiple simulations of the same protein (e.g., different variants). To run the script, use the following syntax:

```
./hbondkernel.py hbond1.xvg hbond2.xvg ...
```

Include as many `.xvg` files as needed for comparison.

