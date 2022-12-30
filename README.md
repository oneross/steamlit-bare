# Notes

Followed example [here](https://www.artefact.com/blog/how-to-deploy-and-secure-your-streamlit-app-on-gcp/) somewhat.

Followed [this](https://maelfabien.github.io/project/Streamlit/#) excellent writeup for dockerfile after failing for 5 iterations.  was also inspired nby jekyll setup.

Ultimately switched from gcr to artifact registry as was getting timeouts

```
gcloud run deploy SERVICE --source .
```
