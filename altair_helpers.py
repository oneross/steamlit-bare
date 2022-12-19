import altair as alt

def get_heatmap_with_counts(df, xCol, yCol):
    skinny = df[[yCol, xCol]]
    skinny2 = skinny.query(xCol + ' == ' + xCol + ' and ' + yCol + ' == ' + yCol)
    skinny2[xCol] = skinny2[xCol].astype(str)
    skinny2[yCol] = skinny2[yCol].astype(str)
  

    base = alt.Chart(skinny2).transform_aggregate(
        num_tasks='count()',
        groupby=[yCol, xCol]
    ).encode(
        alt.X(xCol, scale=alt.Scale(paddingInner=0)),
        alt.Y(yCol, scale=alt.Scale(paddingInner=0)),
    )

    heatmap = base.mark_rect().encode(
        color=alt.Color('num_tasks:Q',
            scale=alt.Scale(scheme='viridis'),
            legend=None
        )
    )

    text = base.mark_text(baseline='middle').encode(
        text='num_tasks:Q',
        color=alt.condition(
            alt.datum.num_tasks > 4,
            alt.value('black'),
            alt.value('white')
        )
    )

    return (heatmap, text)